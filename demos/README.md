# Demo Images and Videos

This folder contains local demo media for your portfolio projects.

## How to Add Media

1. For each project, create a folder named after the project ID:
   - `cardiac/` - Cardiac Function Assessment
   - `cloud/` - Cloud Computing
   - `hotel/` - Hotel Rating Prediction
   - `cancer/` - Multi-Cancer Classification
   - `encryption/` - Classical Encryption Package
   - `social/` - Social App
   - `shop/` - Shop App
   - `bookly/` - Bookly
   - `news/` - News App
   - `buying/` - BuyingApp

2. In each project folder, create a `manifest.json` file with this structure:

```json
{
  "images": [
    {
      "name": "Descriptive name for the image",
      "url": "filename.png"
    }
  ],
  "videos": [
    {
      "name": "Descriptive name for the video",
      "url": "filename.mp4"
    }
  ]
}
```

3. Place your actual image and video files in the same folder as the manifest.json

## File Structure Example

```
demos/
├── cardiac/
│   ├── manifest.json
│   ├── home_screen.png
│   ├── analysis_results.png
│   └── app_demo.mp4
├── news/
│   ├── manifest.json
│   ├── news_feed.png
│   └── article_view.png
└── README.md
```

## Supported File Types

- Images: .png, .jpg, .jpeg, .gif, .webp, .bmp, .svg
- Videos: .mp4, .webm, .mov, .ogg

## Benefits of Local Storage

- ✅ No GitHub API rate limits
- ✅ Faster loading
- ✅ No network dependencies
- ✅ Full control over media organization
- ✅ Works offline (when served locally)