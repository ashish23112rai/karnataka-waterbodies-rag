import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
import chromadb

# Load GeoJSON file
data_path = "data/DWA Waterbodies Ph1 for Karnataka.geojson"
gdf = gpd.read_file(data_path)

st.title("Karnataka Water Bodies Viewer – Environmental RAG Demo")

# Display number of water bodies
st.write(f"Loaded {len(gdf)} water bodies.")

# Show quick map visualization of all water bodies
st.map(gdf)

# Prepare dataframe for display by converting geometry to string
gdf_display = gdf.copy()
gdf_display["geometry"] = gdf_display["geometry"].astype(str)

# Display the sample data table
st.write("Sample of Water Bodies Data:")
st.dataframe(gdf_display.head())

# Plot a detailed map with matplotlib and show in Streamlit
st.write("Geographic Distribution of Water Bodies:")
fig, ax = plt.subplots(figsize=(8,8))
gdf.plot(ax=ax, color="blue", alpha=0.5, edgecolor="k")
plt.axis("equal")
st.pyplot(fig)

# Initialize embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Chroma client and collection (create if not exists)
#client = chromadb.PersistentClient(path="./chromadb_data")
client = chromadb.Client()
collection = client.get_or_create_collection(name="karnataka_waterbodies")

# User input for query
query = st.text_input("Enter your query about Karnataka water bodies:")

if query:
    # Embed user query
    query_embedding = embedder.encode(query).tolist()

    # Query Chroma for top 5 relevant documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        include=["documents", "metadatas", "distances"]
    )

    st.write(f"Top {len(results['documents'][0])} results for your query:")

    # For mapping the retrieved results
    result_coords = []
    result_labels = []

    # Display results with formatted metadata and interactive map
    for i, (doc, meta, dist) in enumerate(zip(results["documents"][0], results["metadatas"][0], results["distances"][0])):
        name = meta.get("name") if meta.get("name") and meta.get("name").strip() else "Unknown"
        wbtype = meta.get("type") if meta.get("type") else "Unknown"
        village = meta.get("village") if meta.get("village") else "Unknown"
        district = meta.get("district") if meta.get("district") else "Unknown"
        area = meta.get("area")
        area_text = f"{area:.2f} sq km" if isinstance(area, (float, int)) else "Unknown area"
        river = meta.get("river") if meta.get("river") else "Unknown"
        basin = meta.get("basin") if meta.get("basin") else "Unknown"
        rural_urban = meta.get("rural_urban")
        rural_urban_text = rural_urban if rural_urban and rural_urban.strip() else "Unknown classification"
        ownership = meta.get("ownership")
        ownership_text = ownership if ownership and ownership.strip() else "Unknown ownership"
        lat = meta.get("latitude")
        lon = meta.get("longitude")

        # Save for result mapping if coordinates exist
        if lat and lon and isinstance(lat, (float, int)) and isinstance(lon, (float, int)):
            result_coords.append({"lat": float(lat), "lon": float(lon)})
            label = f"{name}, {village}, {district}"
            result_labels.append(label)

        st.markdown(f"### Result {i+1} (Distance: {dist:.4f})")
        st.markdown(
            f"**Name:** {name}  \n"
            f"**Type:** {wbtype}  \n"
            f"**Location:** {village}, {district}, Karnataka  \n"
            f"**Area:** {area_text}  \n"
            f"**River:** {river}  \n"
            f"**Basin:** {basin}  \n"
            f"**Classification:** {rural_urban_text}  \n"
            f"**Ownership:** {ownership_text}  \n"
            f"**Coordinates:** ({lat}, {lon})"
        )
        st.write("---")

    # Show the retrieved results on a map
    if result_coords:
        import pandas as pd
        map_df = pd.DataFrame(result_coords)
        st.write("Locations of retrieved water bodies:")
        st.map(map_df)
