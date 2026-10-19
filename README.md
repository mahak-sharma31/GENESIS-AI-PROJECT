# GENESIS AI — Budget-Aware Invention Studio

A local Flask prototype for an AI Expo demonstration. The default engine is offline and rule-based; no API key is needed. It matches six supported sample problems and can produce a general tracking concept for other unmatched inputs. It does not guarantee a technically complete solution for every possible problem.

## Run in VS Code (Windows)
1. Extract the ZIP and open the `GENESIS_AI_Project` folder in VS Code.
2. Open Terminal and run:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   python app.py
   ```
3. Open `http://127.0.0.1:5000`.

## Budget and category behavior
- Six sample cards use different suggested budgets; each budget can be edited.
- Category is inferred from the title and description.
- The backend recalculates the itemised cost and will not display a total above the entered budget.
- If the full material list does not fit, it may show a clearly labelled simplified proof-of-concept using listed reusable/affordable items. If no listed item fits, it says the build is not feasible at that budget rather than claiming a complete build costs zero.
- Prices are illustrative estimates, not live-verified store prices.

## Important limitation
This is a deterministic, rule-based demonstration, not a general-purpose generative AI model. The offline engine supports a limited set of patterns. For unrelated or novel problems it may offer a general tracking concept; validate any design, cost and safety before construction.

## Optional Gemini mode
The project can optionally use Gemini if you configure a valid API key in a local `.env` file. Copy `.env.example` to `.env`, then set `GEMINI_API_KEY` and optionally `GEMINI_MODEL`. Never commit `.env` or share the key. If Gemini is not configured or fails, the app falls back to the offline engine.
