```
#!/bin/sh
ZOT="${ZOT}"

docker pull ${ZOT}/minio/minio:RELEASE.2025-09-07T16-13-09Z
docker pull ${ZOT}/minio/minio:RELEASE.2025-09-07T16-13-09Z-cpuv1
docker pull ${ZOT}/prometheus/prometheus:v3.0.0
docker pull ${ZOT}/grafana/grafana:12.3

docker pull ${ZOT}/library/redis:7
docker pull ${ZOT}/library/postgres:16
docker pull ${ZOT}/dhi.io/argocd:3
```
