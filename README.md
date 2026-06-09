# 🎛️ National School Smart Kitchen Network AI

A data-driven, localized logistics and predictive portion-planning application engineered using Python and Streamlit. This system optimizes ingredient procurement, accurately forecasts student turnout baselines, and implements real-time mitigation strategies to eliminate institutional food waste across multiple secondary school profiles.

---

## 🚀 Key Features

* **Dynamic Multi-School Profiling:** Implements customized baseline profiles for major national institutions (State House Girls' High School, Alliance High School, St. George's Girls' Secondary School, Lenana School, and Nairobi School).
* **Behavior-Driven Turnout Forecasting:** Integrates custom algorithmic multi-school preference factors (e.g., automated portion reductions for low-enthusiasm menus prone to canteen flight risks, and automated boosts for high-demand meals like Saturday Pilau).
* **Zero-Waste Predictive Audit Engine:** Features real-time operational feedback modules including a **Food Wastage Audit** and an **Emergency Shortage Tracker** that output actionable, recursive administrative action items.
* **Granular Raw Ingredient Planner:** Provides sub-module conversions transforming final dynamically calculated portions into precise store-harvest weights in Kilograms (KGs).
* **100% Offline-Proof Execution:** Architected with localized data structures to ensure continuous kitchen operations without internet dependency.

---

## 🛠️ Tech Stack & Architecture

* **Language:** Python 3.10+
* **Framework:** Streamlit (UI & Reactive Layout Execution)
* **Data Processing:** Pandas (Dataframe restructuring and array optimization)
* **Design Pattern:** Modular functional components with secure, scoped multi-widget state keys.

---

## 📦 Local Installation & Setup

To execute this pipeline locally for administrative demonstrations, clone this repository and initialize the Streamlit server:

```bash
# Clone the private repository
git clone [https://github.com/Grace721-spec/shg-smart-kitchen.git](https://github.com/Grace721-spec/shg-smart-kitchen.git)

# Navigate to the project directory
cd shg-smart-kitchen

# Install the required technical dependencies
pip install streamlit pandas

# Initialize the web application local server
streamlit run app.py
