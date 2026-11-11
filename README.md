# 86 the Admin — FFmpeg Video Cutting Service

Lightweight Flask + FFmpeg service deployed on Render.com free tier.
Called by Make.com Scenario 1B to cut and resize video clips for each platform.

## Endpoints

- `GET /health` — returns "ok" (used by Make.com to wake the service)
- `POST /cut` — cuts a clip from a video

## POST /cut payload

```json
{
  "video_url": "https://drive.google.com/uc?id=FILE_ID&export=download",
  "start_seconds": 142.5,
  "end_seconds": 187.0,
  "platform": "instagram",
  "output_name": "week46-clip1-instagram"
}
```

## Platform specs

| platform | width | height | use |
|---|---|---|---|
| instagram | 1080 | 1920 | Reels (9:16) |
| linkedin | 1080 | 1080 | Video posts (1:1) |
| youtube_long | 1920 | 1080 | Long-form (16:9) |
| youtube_short | 1080 | 1920 | Shorts (9:16) |

## Deploy

Push this folder to GitHub, connect to Render.com → New Web Service.
