# Afyamkononi

## Project Setup

1. **Clone the repository**

   ```sh
   git clone https://github.com/Tornshorts/Afyamkononi
   cd Afyamkononi
   ```

2. **Create and activate a virtual environment**

   ```sh
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Install Tailwind CSS CLI**
   - You can install Tailwind CLI globally using npm:
     ```sh
     npm install -g tailwindcss
     ```
   - Or use it locally in your project:
     ```sh
     npm install tailwindcss
     ```

## Running the Project

1. **Set environment variables** (if required)

   - Copy `.env.example` to `.env` and update values as needed.

2. **Run the application**

- Set up database

  ```sh
  flask db init
  ```

  ```sh
  flask db migrate
  ```

  ```sh
  flask db upgrade
  ```

- Run it
  ```sh
  flask run
  ```

3. **Build Tailwind CSS**

   - Open another terminal :
     ```sh
     tailwindcss -i ./src/input.css -o ./static/css/output.css --watch
     ```
