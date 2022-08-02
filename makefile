create_image:
	docker build -t ai4af/tessla:latest . -f docker/Dockerfile
.phony: create_image

run_image:
	docker run --rm ai4af/tessla:latest
.phone: run_image

run_simulate_competition:
	docker run -v /Users/kuba/Desktop/test_inputs:/input:ro -v :/output -it ai4af/tessla:latest
.phone: run_simulate_competition
