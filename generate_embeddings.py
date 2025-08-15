import geopandas as gpd
from sentence_transformers import SentenceTransformer
import chromadb

# Load GeoJSON
gdf = gpd.read_file("data/DWA Waterbodies Ph1 for Karnataka.geojson")

embedder = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./chromadb_data")
collection = client.get_or_create_collection(name="karnataka_waterbodies")

texts = []
metadatas = []
for idx, row in gdf.iterrows():
    name = row.get('waterbody_', 'unknown')  # Main waterbody name column
    wbtype = row.get('waterbod_1', 'unknown')  # Type/category
    district = row.get('district', 'unknown')
    village = row.get('village', 'unknown')
    latitude = row.get('latitude', 'unknown')
    longitude = row.get('longitude', 'unknown')
    area = row.get('gis_area', row.get('st_area_shape_', 'unknown'))
    river = row.get('river', 'unknown')
    basin = row.get('basin', 'unknown')
    rural_urban = row.get('rural_urba', 'unknown')
    ownership = row.get('ownership', 'unknown')
    # Build descriptive chunk
    text = (
        f"Waterbody '{name}', type: {wbtype}, located in {village} village, {district} district, Karnataka. "
        f"Latitude: {latitude}, Longitude: {longitude}, Area: {area} sq km. "
        f"River: {river}, Basin: {basin}, Rural/Urban: {rural_urban}, Ownership: {ownership}."
    )
    texts.append(text)
    metadatas.append({
        "name": name, "type": wbtype, "district": district, "village": village,
        "latitude": latitude, "longitude": longitude, "area": area, "river": river, "basin": basin,
        "rural_urban": rural_urban, "ownership": ownership
    })

embeddings = embedder.encode(texts).tolist()

def batch(iterable, n=1000):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

max_batch_size = 5000
ids = [str(i) for i in range(len(texts))]
for text_batch, embed_batch, meta_batch, id_batch in zip(
    batch(texts, max_batch_size),
    batch(embeddings, max_batch_size),
    batch(metadatas, max_batch_size),
    batch(ids, max_batch_size)
):
    collection.add(
        documents=text_batch,
        embeddings=embed_batch,
        metadatas=meta_batch,
        ids=id_batch
    )

print(f"Added {len(texts)} waterbody embeddings to ChromaDB.")
