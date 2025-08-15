
# Karnataka Water Bodies Retrieval-Augmented Generation (RAG) System

This project is an environmental Geographic Information RAG system focused on water bodies in Karnataka, India. It combines geographic data, satellite imagery, and location-based information to answer spatial and semantic queries, providing location-specific insights about lakes, reservoirs, rivers, and other water features.

---

## Features

- Semantic search over water body data using state-of-the-art sentence embeddings
- Retrieval of relevant waterbody information with rich metadata (name, type, district, area, river, ownership, etc.)
- Interactive geographic visualizations with maps of all water bodies and query result locations
- Persistent vector storage with ChromaDB for fast and accurate similarity search
- Simple, user-friendly web interface built with Streamlit

---

## Data Source

The water bodies dataset is derived from Karnataka state government GeoJSON data:

- Source: [DWA Waterbodies Ph1 for Karnataka](https://indiawris.gov.in/downloads/)
- Includes detailed attributes like village, district, river basin, waterbody type, ownership, coordinates, and area

---

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/karnataka-waterbodies-rag.git
cd karnataka-waterbodies-rag

2. Create and activate a Python virtual environment:
python3 -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate


3. Install dependencies:
pip install -r requirements.txt


4. Generate embeddings (run once before starting the app):
python generate_embeddings.py


5. Run the Streamlit app:
streamlit run app.py


---

## Usage

Enter natural language queries about Karnataka water bodies in the input box. The system retrieves the top 5 most relevant entries based on semantic similarity and displays detailed information along with their locations on interactive maps.

---

## Example Queries

Try asking the following or similar questions:

- "List rivers in Mysore district"
- "Show lakes in rural areas"
- "Find water bodies owned by government"
- "Water bodies near Bangalore with large area"
- "Reservoirs suitable for irrigation"
- "Water bodies in coastal Karnataka"
- "Identify ponds in Tumkur village"
- "Major basins in Karnataka"
- "River waterbodies in Mandya district"
- "Show tanks in urban locations"
- "Find water bodies renovated recently"
- "Reservoirs in the Krishna basin"
- "Lakes near Dharwad"
- "All water bodies in Bangalore district"
- "Find water bodies accessed for fishing"
- "List private water bodies in Karnataka"
- "Water bodies with highest storage capacity"

---

## Project Structure

- `app.py` — Main Streamlit application with UI, search, and visualization
- `generate_embeddings.py` — Script to create embeddings and store them in ChromaDB
- `data/` — Folder containing Karnataka water bodies GeoJSON data
- `requirements.txt` — Python dependencies
- `README.md` — This file

---

## Technical Details

- **Embedding Model:** HuggingFace Sentence Transformers (`all-MiniLM-L6-v2`)
- **Vector Store:** ChromaDB with persistent storage for fast semantic retrieval
- **Geospatial Processing:** GeoPandas for loading, manipulating, and visualizing geographic data
- **Visualization:** Streamlit interactive maps and matplotlib plots
- **Deployment:** Easily deployable on Streamlit Cloud or HuggingFace Spaces

---

## Future Improvements

- Add advanced spatial filtering (e.g., radius search near a city)
- Incorporate satellite image analysis for up-to-date land/water cover
- Integrate a conversational LLM to generate natural language summaries or answers
- Enhance UI with map-based query selectors and filters

---

## License

This project is for educational purposes as part of a Geographic Information RAG assignment.

---

Thank you for exploring Karnataka’s water resources with this RAG system!