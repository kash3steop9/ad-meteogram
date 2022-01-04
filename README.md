# Meteogram Service for AppDaemon

This automatically updates a [Meteograms image](https://meteograms.com) once a day.

```yaml
meteogram:
  module: meteogram
  class: MeteogramService
  dependencies: sentry
```

You can then render it with a simple picture card:

```yaml
type: picture
image: /local/meteograms/meteogram.png
```
