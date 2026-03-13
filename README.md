# Portable Zot Service

## Installation

```shell
# 최신 버전 확인 후 다운로드 (x86_64 기준)
curl -Lo zot https://github.com/project-zot/zot/releases/latest/download/zot-linux-amd64

# 실행 권한 부여 및 경로 이동
chmod +x zot
sudo mv zot /usr/local/bin/zot
```

## Configuration

다음과 같이 `/etc/zot/config.json` 파일을 작성합니다. 5000 포트는 Coder가 사용하므로 포트 충돌이 나지 않도록 확인하도록 합니다.

```json
{
  "distSpecVersion": "1.1.0",
  "storage": {
    "rootDirectory": "/var/lib/zot",
    "gc": true
  },
  "http": {
    "address": "0.0.0.0",
    "port": "5000",
    "tls": {
      "cert": "/etc/zot/certs/dev-server/dev-server.crt",
      "key": "/etc/zot/certs/dev-server/dev-server.key"
    }
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
            { "prefix": "**" }
          ]
        },
        {
          "urls": ["https://quay.io"],
          "onDemand": true,
          "content": [
            { "prefix": "**" }
          ]
        },
        {
          "urls": ["https://gcr.io"],
          "onDemand": true,
          "content": [
            { "prefix": "**" }
          ]
        },
        {
          "urls": ["https://ghcr.io"],
          "onDemand": true,
          "content": [
            { "prefix": "**" }
          ]
        },
        {
          "urls": ["https://mcr.microsoft.com"],
          "onDemand": true,
          "content": [
            { "prefix": "**" }
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

에러 발생시 다음의 커맨드로 체크합니다.

```shell
journalctl -u zot.service -n 20 --no-pager
```

## Use

### Docker 설정

`/etc/docker/daemon.json` 파일에 다음과 같이 추가합니다.

```json
{
  "insecure-registries": ["<ZOT_IP>:5000"]
}
```

### Helm Chart의 `values.yaml`

```yaml
repository: <ZOT_IP>:5000/bitnami/postgresql
```

### OCI 방식의 Helm Chart 호출

```shell
helm pull oci://<ZOT_IP>:5000/bitnamicharts/postgresql
```

### Warming Up

```shell
# Docker Hub 공식 이미지
docker pull <ZOT_IP>:5000/library/nginx:latest

# Bitnami 이미지
docker pull <ZOT_IP>:5000/bitnami/postgresql:17

# ArgoCD (GHCR)
docker pull <ZOT_IP>:5000/argoproj/argocd:v2.10.0

# Helm Chart (OCI)
helm pull oci://<ZOT_IP>:5000/bitnamicharts/postgresql --version 16.0.0
```
