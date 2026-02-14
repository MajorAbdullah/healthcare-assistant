.PHONY: all start stop install install-backend install-frontend backend frontend clean

# Start everything with: make start
all: start

# Install all dependencies
install: install-backend install-frontend

install-backend:
	pip install -r requirements.txt

install-frontend:
	cd Frontend && npm install

# Start both backend and frontend
start:
	@echo "Starting Health Buddy..."
	@echo "Backend  → http://localhost:8000"
	@echo "Frontend → http://localhost:5173"
	@echo "API Docs → http://localhost:8000/docs"
	@echo ""
	@trap 'kill 0' INT TERM; \
	python3 api/main.py & \
	cd Frontend && npm run dev & \
	wait

# Start services individually
backend:
	python3 api/main.py

frontend:
	cd Frontend && npm run dev

# Stop all running services
stop:
	@-pkill -f "python api/main.py" 2>/dev/null
	@-pkill -f "vite" 2>/dev/null
	@echo "Services stopped."

# Build frontend for production
build:
	cd Frontend && npm run build

# Clean build artifacts
clean:
	rm -rf Frontend/dist Frontend/node_modules/.vite
