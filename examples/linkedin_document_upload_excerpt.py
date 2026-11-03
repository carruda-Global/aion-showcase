# EXCERPT of aion/integrations/linkedin/tools.py - LinkedIn Documents API (carousel PDF upload)
    async def upload_document(self, data: bytes, filename: str) -> dict:
        profile = await self.get_profile()
        owner = f"urn:li:person:{profile.get('sub', '')}"
        init = await self._post(
            "/documents?action=initializeUpload",
            {"initializeUploadRequest": {"owner": owner}},
            restli=True,
        )
        if "error" in init:
            return init
        value = init.get("value", {})
        upload_url, asset = value.get("uploadUrl"), value.get("document")
        if not upload_url or not asset:
            return {"error": "initializeUpload sem uploadUrl/document", "detail": str(init)[:300]}
        await self.oauth.ensure_token()
        async with httpx.AsyncClient() as client:
            resp = await client.put(
                upload_url,
                content=data,
                headers={"Authorization": f"Bearer {self.oauth.access_token}"},
                timeout=60,
            )
        if resp.status_code not in (200, 201):
            logger.error(f"Document upload failed {resp.status_code}: {resp.text[:300]}")
            return {"error": f"upload error {resp.status_code}", "detail": resp.text[:300]}
        logger.info(f"Document uploaded: {asset} ({filename})")
        return {"asset": asset}

    async def create_carousel_post(self, text: str, document_asset: str, title: str = "") -> dict:
        profile = await self.get_profile()
        post_data = {
            "author": f"urn:li:person:{profile.get('sub', '')}",
            "commentary": text[:3000],
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "content": {"media": {"title": title[:200], "id": document_asset}},
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        }
        result = await self._post("/posts", post_data, restli=True)
        if "error" in result:
            return result
        post_id = result.get("id", "")
        logger.info(f"Carousel post created: {post_id}")
        return {
            "status": "published",
            "post_id": post_id,
            "url": f"https://www.linkedin.com/feed/update/{post_id}",
        }

