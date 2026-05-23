# dCrypt - Real-Time Gamified Cryptic Hunt Platform
This Python-based web application is a highly interactive, real-time cryptic hunt and Capture-The-Flag (CTF) platform built using Django. Unlike traditional trivia sites, it integrates advanced **game-theory mechanics**—including troop combat, passive point generation, shields, and strategic poisons—to deliver a deeply engaging and highly competitive user experience.
The platform uses **Django Channels (WebSockets)** to establish persistent, low-latency connections with active players, enabling instant victim notifications when attacks occur. Additionally, a custom **daemon thread scheduler** runs continuously in the background to handle passive points generation and time-based status updates. Built with a "security-first" approach, it includes server-side transaction protection, regex-based anti-cheat checks, IP rate-limiting, and comprehensive logging hooked into external **Discord Webhooks** for real-time administrator telemetry.
This project solves the problem of standard static question-and-answer trivia portals by introducing dynamic PvP (Player vs. Player) mechanics and real-time multiplayer states, turning a traditional cryptic hunt into a strategic virtual war game.
## How It Works
1. **Trivia Progression**: Users solve challenging cryptography and riddle-based questions to earn *Battle Points* (BP).
2. **Economic Shop**: Earned BP functions as in-game currency, which players spend in the shop to purchase military troops (soldiers, tanks, bombers, anti-aircraft guns) or tactical power-ups (multipliers, poisons, shields, discount coupons).
3. **Passive Income Generation**: A background thread continuously increments player *Flag Points* (FP) passively every hour, which determines the live leaderboard rankings.
4. **PvP Combat & Strategy**:
   * **Attack**: Players deploy their bought troops to attack rival teams. The system calculates the total Attack Points (AP) versus the victim's Defense Points (DP).
   * **Outcome**: A winning attack steals **50% of the victim's total Flag Points**, while a failed attack penalizes the attacker, giving **25% of their Flag Points** to the defender.
   * **Shields & Poison**: Players can activate hourly shields to block upcoming attacks or buy poisons to freeze an opponent's passive point accumulation for 3 hours.
5. **Real-Time Synchronization**: When a team is attacked or poisoned, a WebSocket message is instantly pushed to their active browser session to update their interface, alongside a mobile push alert dispatched to their team's Discord server.
## Features
* **Real-Time Gamification**: Implements a complete Strategy/PvP game loop featuring troop combat calculations, active item cooldowns, and tactical points-stealing.
* **WebSocket Integration**: Uses Django Channels for real-time notifications and instant site-wide combat log updates.
* **Asynchronous Scheduling**: Features a robust, non-blocking background daemon thread (`hourlyfp`) executing every second to manage hourly points accumulation, shield decays, and poison expirations.
* **Hardened Security & Anti-Cheat**: 
  * Enforces IP-based rate limiting via `django-ratelimit` on all interactive endpoints to prevent brute-forcing.
  * Sanitizes inputs with regex-based security filters to capture and log SQL/script injection attempts.
  * Performs strict server-side validation on shop checkouts to prevent parameter manipulation (e.g., purchasing negative items or using fake currency).
* **Multi-Channel Discord Telemetry**: Integrates with multiple Discord Webhooks to instantly alert game admins of solved questions, suspicious exploits, combat records, and system-wide notifications.
## Requirements
* Python 3.10+
* SQLite3 (for local development) or PostgreSQL (configured for production)
* Python packages:
  * `django`
  * `channels`
  * `django-ratelimit`
  * `whitenoise`
  * `gspread`
  * `requests`
## Usage
### 1. Install Dependencies
Set up a python virtual environment and install the required modules:
```bash
python -m venv venv
venv\Scripts\activate      # On Windows
source venv/bin/activate    # On Unix/macOS
pip install django channels django-ratelimit whitenoise gspread requests
```
### 2. Configure Database & Migrations
Initialize the local SQLite database schemas:
```bash
python manage.py makemigrations users questions
python manage.py migrate --fake-initial
```
### 3. Create Admin & Test Accounts
Generate administrative credentials and test player accounts:
```bash
# Generate a superuser for django backend (/admin/)
python manage.py createsuperuser
```
### 4. Run the Platform Locally
Launch the development server:
```bash
python manage.py runserver
```
Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web browser to play the game!
## Notes
* **Mocked Integrations**: The project includes a local custom stub for the Discord API to bypass standard compilation overheads and allow offline testing without active webhook links.
* **Database Fallback**: The development configuration is set to automatically run on a local `db.sqlite3` instance when booted in `DEBUG = True` mode, keeping it isolated from any live production PostgreSQL servers.
* **Competitive Integrity**: The codebase serves as an excellent demonstration of full-stack defensive coding, showing how to safely tie WebSockets, transactional database operations, and anti-cheat validations into a single cohesive system.
