import asyncio
import logging
import time
from datetime import datetime, time as dtime

from aion.integrations.linkedin import LinkedInIntegration
from aion.integrations.linkedin.config import LinkedInConfig
from aion.content_bank.engine import escolher_variacao, registrar_publicacao
from aion.content_bank.engagement import calcular_pesos_topico
from aion.content_bank.carousel import publicar_carrossel
from aion.leads.tracker import gerar_url_tracking, obter_metricas_engajamento

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("linkedin-sales-machine")

HORARIOS = [
    {"hora": 8,  "tipo": "post_manha"},
    {"hora": 12, "tipo": "post_almoco"},
    {"hora": 15, "tipo": "post_tarde"},
    {"hora": 17, "tipo": "carrossel"},
]
INTERVALO_VERIFICACAO = 600
INTERVALO_ANALISE_ENG = 3600
MAX_ERROS_PAUSA = 10
PAUSA_ERRO = 21600


class LinkedInSalesMachine:
    def __init__(self):
        self.linkedin: LinkedInIntegration | None = None
        self.running = False
        self.erros = 0
        self.posts_hoje: dict[str, bool] = {}
        self.carrossel_hoje = False
        self.dia_atual = datetime.now().day
        self.ultima_analise_engajamento = 0.0
        self.pesos_topico: dict[str, float] = {}

    def resetar_dia(self):
        hoje = datetime.now().day
        if hoje != self.dia_atual:
            self.posts_hoje = {}
            self.carrossel_hoje = False
            self.dia_atual = hoje
            self.erros = 0

    def dia_util(self) -> bool:
        return datetime.now().weekday() < 5

    def tipos_pendentes(self) -> list[dict]:
        self.resetar_dia()
        if not self.dia_util():
            return []
        now = datetime.now()
        pendentes = []
        for h in HORARIOS:
            tipo = h["tipo"]
            if tipo == "carrossel":
                if not self.carrossel_hoje and now.hour >= h["hora"]:
                    pendentes.append(h)
            else:
                if not self.posts_hoje.get(tipo) and now.hour >= h["hora"]:
                    pendentes.append(h)
        return pendentes

    async def analisar_engajamento(self):
        if not self.linkedin:
            return
        try:
            pesos = await calcular_pesos_topico(self.linkedin)
            if pesos:
                self.pesos_topico = pesos
                logger.info(f"Pesos por topico atualizados: {pesos}")
        except Exception as e:
            logger.warning(f"Falha ao analisar engajamento: {e}")

    async def publicar_post(self, horario: dict) -> bool:
        tipo_label = horario["tipo"]
        try:
            variacao = escolher_variacao(self.pesos_topico, tipo=tipo_label)
            texto = variacao["texto"]
            topico = variacao["topico"]
            link = gerar_url_tracking(
                base_url="https://global-engenharia.com/ecosystem",
                post_id="",
                topico_id=topico["id"],
                utm_campaign=topico["utm"],
                utm_content=tipo_label,
            )

            result = await self.linkedin.tools.create_post(text=texto)
            if "error" in result:
                logger.error(f"[{tipo_label}] Erro ao postar: {result['error']}")
                self.erros += 1
                return False

            post_id = result.get("post_id", "")
            if post_id:
                await self.linkedin.tools.create_comment(post_id=post_id, text=link + " — Acesse para saber mais.")
                registrar_publicacao(post_id, topico["id"], tipo_label, result.get("url", ""))
                logger.info(f"[{tipo_label}] Publicado: {topico['id']} | combo: {variacao['combo_id']} | post_id: {post_id}")
            else:
                logger.warning(f"[{tipo_label}] Post criado (201) mas sem post_id no header — comentario nao adicionado")

            self.posts_hoje[tipo_label] = True
            self.erros = 0
            return True

        except Exception as e:
            logger.error(f"[{tipo_label}] Excecao: {e}")
            self.erros += 1
            return False

    async def publicar_carrossel_diario(self) -> bool:
        try:
            result = await publicar_carrossel(self.pesos_topico)
            if result.get("published"):
                self.carrossel_hoje = True
                self.erros = 0
                logger.info(f"[carrossel] Publicado: {result.get('topico', '?')} | post_id: {result.get('post_id', '')}")
                return True
            else:
                logger.error(f"[carrossel] Falha: {result.get('error', 'desconhecido')}")
                self.erros += 1
                return False
        except Exception as e:
            logger.error(f"[carrossel] Excecao: {e}")
            self.erros += 1
            return False

    async def publicar_metricas_semanais(self):
        if datetime.now().weekday() == 0 and datetime.now().hour == 7:
            try:
                metricas = obter_metricas_engajamento(dias=7)
                logger.info(f"Metricas da semana: {metricas}")
                clicks = metricas.get("total_clicks", 0)
                visitantes = metricas.get("visitantes_com_lead", 0)

                if clicks > 0 or visitantes > 0:
                    texto = (
                        f"Metricas desta semana:\n\n"
                        f"Cliques: {clicks}\n"
                        f"Visitantes unicos: {metricas.get('total_visitantes', 0)}\n"
                        f"Leads identificados: {visitantes}\n\n"
                        f"Topicos com mais engajamento:\n"
                    )
                    for topico, count in sorted(
                        metricas.get("clicks_por_topico", {}).items(),
                        key=lambda x: x[1], reverse=True,
                    )[:3]:
                        texto += f"- {topico}: {count} cliques\n"

                    texto += "\nQuer ver como transformar isso em vendas? Link nos comentarios."
                    await self.linkedin.tools.create_post(text=texto)
            except Exception as e:
                logger.debug(f"Falha ao publicar metricas: {e}")

    async def start(self):
        cfg = LinkedInConfig()
        self.linkedin = LinkedInIntegration(config=cfg)
        await self.linkedin.initialize()
        self.running = True

        logger.info("=" * 60)
        logger.info("  LINKEDIN SALES MACHINE - 4 CONTEUDOS/DIA")
        logger.info("  08:00 - Post manha (banco 200 variacoes)")
        logger.info("  12:00 - Post almoco (banco 200 variacoes)")
        logger.info("  15:00 - Post tarde (banco 200 variacoes)")
        logger.info("  17:00 - Carrossel PDF (6 slides)")
        logger.info("  + Feedback de engajamento")
        logger.info("  + Tracking de cliques e leads")
        logger.info("=" * 60)
        logger.info("Banco de 200 variacoes (20 topicos x 10 hooks)")

        from aion.content_bank.engine import total_variacoes, variacoes_restantes
        logger.info(f"Banco de conteudo: {total_variacoes()} variacoes")
        logger.info(f"Variacoes restantes: {variacoes_restantes()}")

        while self.running:
            try:
                if self.erros >= MAX_ERROS_PAUSA:
                    logger.warning(f"Muitos erros ({self.erros}). Pausando {PAUSA_ERRO // 3600}h...")
                    await asyncio.sleep(PAUSA_ERRO)
                    self.erros = 0

                agora = time.time()
                if agora - self.ultima_analise_engajamento > INTERVALO_ANALISE_ENG:
                    logger.info("Analisando engajamento dos posts anteriores...")
                    await self.analisar_engajamento()
                    self.ultima_analise_engajamento = agora

                pendentes = self.tipos_pendentes()
                if pendentes:
                    for h in pendentes:
                        now = datetime.now()
                        logger.info(f"Publicando [{h['tipo']}] as {now.strftime('%H:%M')}")
                        if h["tipo"] == "carrossel":
                            await self.publicar_carrossel_diario()
                        else:
                            await self.publicar_post(h)
                        await asyncio.sleep(30)
                else:
                    posts_count = len(self.posts_hoje) + (1 if self.carrossel_hoje else 0)
                    if self.dia_util():
                        logger.info(f"{posts_count}/4 conteudos hoje. Proxima verificacao em {INTERVALO_VERIFICACAO // 60}min.")
                    else:
                        logger.info("Fim de semana — sem publicacao.")

                await self.publicar_metricas_semanais()
                await asyncio.sleep(INTERVALO_VERIFICACAO)

            except Exception as e:
                self.erros += 1
                logger.error(f"Erro no loop principal: {e}", exc_info=True)
                await asyncio.sleep(300)

    async def stop(self):
        self.running = False
        if self.linkedin:
            await self.linkedin.shutdown()
        logger.info("LinkedIn Sales Machine stopped.")


async def run_tracking_server():
    try:
        import uvicorn
        from fastapi import FastAPI
        from aion.leads.router import router

        app = FastAPI(title="LinkedIn Tracking")
        app.include_router(router)
        config = uvicorn.Config(app, host="0.0.0.0", port=8421, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()
    except Exception as e:
        logger.info(f"Tracking server not started (optional): {e}")


async def main():
    agent = LinkedInSalesMachine()

    tracking_task = asyncio.create_task(run_tracking_server())

    try:
        await agent.start()
    except KeyboardInterrupt:
        logger.info("Shutdown requested...")
        await agent.stop()
        tracking_task.cancel()
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
