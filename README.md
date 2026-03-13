# Portable Zot Service

## Installation

```
# 최신 버전 확인 후 다운로드 (x86_64 기준)
curl -Lo zot https://github.com/project-zot/zot/releases/latest/download/zot-linux-amd64

# 실행 권한 부여 및 경로 이동
chmod +x zot
sudo mv zot /usr/local/bin/zot
```

## Configuration

다음과 같이 `/etc/zot/config.json` 파일을 작성합니다.

```json
{
  "distSpecVersion": "1.1.0",
  "storage": {
    "rootDirectory": "/var/lib/zot",
    "gc": true
  },
  "http": {
    "address": "0.0.0.0",
    "port": "5000"
  },
  "log": {
    "level": "info"
  },
  "extensions": {
    "sync": {
      "enable": true,
      "registries": [
        {
          "urls": ["https://registry-1.docker.io"],
          "onDemand": true,
          "content": [
            { "source": "library/*", "destination": "/library/*" },
            { "source": "bitnami/*", "destination": "/bitnami/*" },
            { "source": "bitnamicharts/*", "destination": "/bitnamicharts/*" }
          ]
        },
        {
          "urls": ["https://quay.io"],
          "onDemand": true,
          "content": [
            { "source": "prometheus/*", "destination": "/prometheus/*" },
            { "source": "grafana/*", "destination": "/grafana/*" },
            { "source": "coreos/*", "destination": "/coreos/*" }
          ]
        },
        {
          "urls": ["https://gcr.io"],
          "onDemand": true,
          "content": [
            { "source": "google-containers/*", "destination": "/google-containers/*" },
            { "source": "kaniko-project/*", "destination": "/kaniko-project/*" }
          ]
        },
        {
          "urls": ["https://ghcr.io"],
          "onDemand": true,
          "content": [
            { "source": "argoproj/*", "destination": "/argoproj/*" },
            { "source": "external-secrets/*", "destination": "/external-secrets/*" },
            { "source": "cert-manager/*", "destination": "/cert-manager/*" }
          ]
        },
        {
          "urls": ["https://mcr.microsoft.com"],
          "onDemand": true,
          "content": [
            { "source": "oss/kubernetes/*", "destination": "/oss/kubernetes/*" }
          ]
        }
      ]
    }
  }
}
```

## Systemd Service

`/etc/systemd/system/zot.service` 파일을 다음과 같이 작성합니다.

```
[Unit]
Description=Zot OCI Registry
After=network.target

[Service]
User=root
WorkingDirectory=/var/lib/zot
ExecStart=/usr/local/bin/zot serve /etc/zot/config.json
Restart=always

[Install]
WantedBy=multi-user.target
```

## Use

### Docker 설정

`/etc/docker/daemon.json` 파일에 다음과 같이 추가합니다.

```
{
  "insecure-registries": ["<ZOT_IP>:5000"]
}
```

### Helm Chart의 `values.yaml`

```
repository: <ZOT_IP>:5000/bitnami/postgresql
```

### OCI 방식의 Helm Chart 호출

```
helm pull oci://<ZOT_IP>:5000/bitnamicharts/postgresql
```

### Warming Up

```
# Docker Hub 공식 이미지
docker pull <ZOT_IP>:5000/library/nginx:latest

# Bitnami 이미지
docker pull <ZOT_IP>:5000/bitnami/postgresql:17

# ArgoCD (GHCR)
docker pull <ZOT_IP>:5000/argoproj/argocd:v2.10.0

# Helm Chart (OCI)
helm pull oci://<ZOT_IP>:5000/bitnamicharts/postgresql --version 16.0.0
```
