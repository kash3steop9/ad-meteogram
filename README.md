# Meteogram Service for AppDaemon

This automatically updates a [Meteograms image](https://meteograms.com) once a day.

```yaml
meteogram:
  module: meteogram
  class: MeteogramService
  dependencies: sentry
  token: !secret meteogram_token
  placeName: Home
```

You can then render it with a simple picture card:

```yaml
type: picture
image: /local/meteograms/meteogram.png
```

Even better, create a camera entity in `configuration.yaml`:

```yaml
camera:
  - platform: generic
    name: Meteogram
    still_image_url: https://127.0.0.1:8123/local/meteograms/meteogram.png
    verify_ssl: false
```
