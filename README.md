# HelloWorldTest

Simple **Hello World** web app built with **Streamlit**, ready to containerize and run on **Amazon ECS**.

## Project files

- `app.py` - Streamlit app entrypoint.
- `requirements.txt` - Python dependencies.
- `Dockerfile` - Container image definition for ECS.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open: `http://localhost:8501`

## Build container image

```bash
docker build -t hello-streamlit:latest .
```

## Run container locally

```bash
docker run --rm -p 8501:8501 hello-streamlit:latest
```

Open: `http://localhost:8501`

## ECS deployment notes

1. Push the image to Amazon ECR.
2. In your ECS task definition, set container port to `8501`.
3. For Fargate, allow inbound traffic on the service/ALB security group to port `8501` (or 80/443 via ALB).
4. Use a health check path of `/`.
