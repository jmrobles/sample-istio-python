# Istio Python instrumentation sample with Opentelemetry SDK

## Instructions

1. Create an virtual env and activate it

```bash
python3 -m venv .
source bin/activate
```
2. Install requirements 

```bash
pip3 install -r requirements.txt
```

3. Start local dev server (for development)

```bash
./run-dev.sh
```

4. Build container

```bash
./build-container.sh
```

5. Tag it for your docker registry or Docker Hub

6. Push it!

7. Modify the `sample-k8s.yaml` with your docker image or use the one included from Docker Hub

8. Create the deployment

9. Open the endpoint in your browser

10. Open the Jaeger Istio dashboard and check for your traces

## Development

Launch all-in-one Jaeger container

```bash
docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 9411:9411 \
  --platform linux/amd64 \
  jaegertracing/all-in-one:1.6
```
## License

MIT License
