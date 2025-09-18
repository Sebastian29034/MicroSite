# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List
from pydantic import BaseModel
from typing import List
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException
import json
from typing import List
import math, re

# Crea UNA sola app y configura CORS inmediatamente
app = FastAPI(title="API Películas Impactantes")

origins = [
    "http://127.0.0.1:5500",  # Live Server (VSCode)
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    # orígenes permitidos (usa "*" solo para pruebas y con allow_credentials=False)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Movie(BaseModel):
    id: int
    titulo: str
    descripcion: str
    image_url: HttpUrl
    video_url: HttpUrl

# Lista de películas (id, título, descripción detallada y URL de imagen pública)
movies: List[Movie] = [
    Movie(
        id=1,
        titulo="Avatar",
        descripcion=(
            "Dirigida por James Cameron. Una épica aventura de ciencia ficción ambientada en Pandora, "
            "donde la explotación humana choca con la cultura Na'vi. Revolucionó efectos visuales y "
            "captura de movimiento, y planteó debates sobre ecología y colonialismo."
        ),
        image_url="https://upload.wikimedia.org/wikipedia/en/d/d6/Avatar_%282009_film%29_poster.jpg",
        video_url="https://www.youtube.com/watch?v=5PSNL1qE6VY"
    ),
    Movie(
        id=2,
        titulo="La La Land",
        descripcion=(
            "Musical romántico de Damien Chazelle que explora sueños, ambición y sacrificio en Los Ángeles. "
            "Combina números musicales estilizados con una historia íntima sobre el costo personal del éxito."
        ),
        image_url="https://upload.wikimedia.org/wikipedia/en/a/ab/La_La_Land_%28film%29.png",
        video_url="https://www.youtube.com/watch?v=0pdqf4P9MB8"
    ),
    Movie(
        id=3,
        titulo="Avengers: Endgame",
        descripcion=(
            "Cierre de la saga Infinity de Marvel. Tras la catástrofe del chasquido, los héroes deben enfrentar "
            "pérdidas y tomar decisiones extremas para restaurar el universo. Emotiva mezcla de acción y homenaje."
        ),
        image_url="https://upload.wikimedia.org/wikipedia/en/0/0d/Avengers_Endgame_poster.jpg",
        video_url="https://www.youtube.com/watch?v=TcMBFSGVi1c"
    ),
    Movie(
        id=4,
        titulo="Titanic",
        descripcion=(
            "Romance épico dirigido por James Cameron que combina una historia de amor imposible con el "
            "relato del trágico hundimiento del trasatlántico Titanic. Fuerte impacto emocional y técnico."
        ),
        image_url="https://m.media-amazon.com/images/M/MV5BYzYyN2FiZmUtYWYzMy00MzViLWJkZTMtOGY1ZjgzNWMwN2YxXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
        video_url="https://www.youtube.com/watch?v=zCy5WQ9S4c0"
    ),
    Movie(
        id=5,
        titulo="Inception",
        descripcion=(
            "Thriller psicológico y de ciencia ficción de Christopher Nolan sobre extracción e inserción de ideas "
            "en sueños. Destaca por su estructura en capas, planteamientos filosóficos sobre la realidad y secuencias de acción imaginativas."
        ),
        image_url="https://m.media-amazon.com/images/M/MV5BZjhkNjM0ZTMtNGM5MC00ZTQ3LTk3YmYtZTkzYzdiNWE0ZTA2XkEyXkFqcGc@._V1_.jpg",
        video_url="https://www.youtube.com/watch?v=YoHD9XEInc0"
    ),
    Movie(
        id=6,
        titulo="The Dark Knight",
        descripcion=(
            "La segunda película de la trilogía de Nolan. Un thriller oscuro donde Batman se enfrenta al Joker, "
            "explorando el orden, el caos y el precio del heroísmo. Aclamada por su guion, dirección y actuación."
        ),
        image_url="https://pics.filmaffinity.com/El_caballero_oscuro-628375729-large.jpg",
        video_url="https://www.youtube.com/watch?v=EXeTwQWrcwY"
    ),
    Movie(
        id=7,
        titulo="Interstellar",
        descripcion=(
            "Odisea espacial de Christopher Nolan que mezcla ciencia, emoción y vínculos familiares. "
            "Aborda viajes interestelares, relatividad temporal y sacrificio humano con imágenes contundentes."
        ),
        image_url="https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg",
        video_url="https://www.youtube.com/watch?v=zSWdZVtXT7E"
    ),
    Movie(
        id=8,
        titulo="The Matrix",
        descripcion=(
            "Clásico de ciencia ficción que revolucionó la acción y la filosofía pop. Sigue a Neo mientras descubre "
            "una realidad simulada y se une a la resistencia. Influyente en efectos visuales y cultura pop."
        ),
        image_url="https://upload.wikimedia.org/wikipedia/en/thumb/d/db/The_Matrix.png/250px-The_Matrix.png",
        video_url="https://www.youtube.com/watch?v=vKQi3bBA1y8"
    ),
    Movie(
        id=9,
        titulo="Gladiator",
        descripcion=(
            "Drama épico sobre un general romano convertido en gladiador que busca venganza y justicia. "
            "Mezcla espectáculos coliseo, honor y política romana con una narrativa poderosa."
        ),
        image_url="https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p24674_p_v13_bc.jpg",
        video_url="https://www.youtube.com/watch?v=owK1qxDselE"
    ),
    Movie(
        id=10,
        titulo="Forrest Gump",
        descripcion=(
            "Película que narra, con sensibilidad e ironía, la vida de Forrest Gump, un hombre de buen corazón "
            "cuyos actos atraviesan eventos históricos de Estados Unidos. Emotiva y cargada de nostalgia."
        ),
        image_url="https://upload.wikimedia.org/wikipedia/en/6/67/Forrest_Gump_poster.jpg",
        video_url="https://www.youtube.com/watch?v=bLvqoHBptjg"
    ),
    Movie(
        id=11,
        titulo="Pulp Fiction",
        descripcion=(
            "Obra central de Quentin Tarantino que entrelaza historias criminales con diálogo afilado y estructura no lineal. "
            "Famosa por su mezcla de violencia estilizada, humor negro y personajes memorables."
        ),
        image_url="https://www.miramax.com/assets/Pulp-Fiction1.png",
        video_url="https://www.youtube.com/watch?v=s7EdQ4FqbhY"
    )

]

@app.get("/")
def root():
    return {"msg": "API Películas Impactantes. Usa /peliculas para listar."}

@app.get("/peliculas", response_model=List[Movie])
def list_movies():
    return movies

@app.get("/peliculas/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    for m in movies:
        if m.id == movie_id:
            return m
    raise HTTPException(status_code=404, detail="Película no encontrada")

##Maps
class Location(BaseModel):
    id: int
    movie_id: int       # id de la película a la que pertenece
    title: str          # nombre del lugar (ciudad/locación)
    description: str    # detalle corto
    lat: float
    lon: float

# Datos de ejemplo (coordenadas aproximadas) — actualízalas si quieres
locations: List[Location] = [
    Location(id=1, movie_id=1, title="Wellington, New Zealand", description="Estudios y localizaciones en Nueva Zelanda (Avatar).", lat=-41.2865, lon=174.7762),
    Location(id=2, movie_id=2, title="Los Ángeles, USA", description="Locaciones en Los Ángeles (La La Land).", lat=34.0522, lon=-118.2437),
    Location(id=3, movie_id=3, title="Atlanta, USA", description="Estudios y rodaje (Avengers: Endgame).", lat=33.7490, lon=-84.3880),
    Location(id=4, movie_id=4, title="Rosarito, Mexico", description="Playa y estudios (Titanic - rodaje de escenas).", lat=32.2719, lon=-117.1225),
    Location(id=5, movie_id=5, title="Los Ángeles, USA", description="Varias escenas y estudios (Inception).", lat=34.0522, lon=-118.2437),
    Location(id=6, movie_id=6, title="Chicago, USA", description="Escenas urbanas (The Dark Knight).", lat=41.8781, lon=-87.6298),
    Location(id=7, movie_id=7, title="Alberta, Canada", description="Paisajes naturales y locaciones (Interstellar).", lat=51.0447, lon=-114.0719),
    Location(id=8, movie_id=8, title="Sydney, Australia", description="Grabaciones y locaciones (The Matrix).", lat=-33.8688, lon=151.2093),
    Location(id=9, movie_id=9, title="Valletta, Malta", description="Localizaciones de época (Gladiator).", lat=35.8989, lon=14.5146),
    Location(id=10, movie_id=10, title="Savannah, USA", description="Localizaciones icónicas (Forrest Gump).", lat=32.0809, lon=-81.0912),
    Location(id=11, movie_id=11, title="Los Ángeles, USA", description="Locaciones en Los Ángeles (Pulp Fiction).", lat=34.0522, lon=-118.2437)
]

@app.get("/ubicaciones", response_model=List[Location], summary="Listar todas las ubicaciones de rodaje")
def list_locations():
    return locations

@app.get("/ubicaciones/{movie_id}", response_model=List[Location], summary="Listar ubicaciones de una película")
def locations_by_movie(movie_id: int):
    result = [l for l in locations if l.movie_id == movie_id]
    if not result:
        raise HTTPException(status_code=404, detail=f"No hay ubicaciones para la película {movie_id}")
    return result


# Modelo para recibir el formulario
class ContactIn(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

@app.post("/contact", status_code=201)
def send_contact(payload: ContactIn):
    """
    Endpoint de ejemplo que recibe un formulario de contacto.
    En producción deberías enviar un email, guardar en DB, o integrar con un servicio.
    Aquí lo registramos en consola y devolvemos un OK.
    """
    # Validación adicional opcional (ejemplo: longitud mínima)
    if len(payload.message.strip()) < 10:
        raise HTTPException(status_code=400, detail="Mensaje demasiado corto (mínimo 10 caracteres).")

    # Acción de ejemplo: guardar en archivo (opcional)
    try:
        with open("contacts.log", "a", encoding="utf-8") as f:
            f.write(f"{payload.name} <{payload.email}> | {payload.subject}\n{payload.message}\n---\n")
    except Exception:
        # no fallamos el endpoint si no puede escribir; solo logueamos
        print("Warning: no se pudo escribir contacts.log")

    print("Contacto recibido:", payload.dict())
    return {"detail": "Mensaje recibido. Gracias!"}

@app.post("/contact")
async def submit_contact(contact: ContactIn):
    with open("contactos.json", "a", encoding="utf-8") as f:
        f.write(contact.json() + "\n")
    return {"message": "Formulario recibido", "data": contact}

# stopwords sencillas (español + inglés)
_STOPWORDS = {
    "y","de","la","el","que","en","los","las","del","con","un","una","por","para","se","sus","su",
    "the","a","an","and","of","in","on","with","is","it","as","by","at","from","this","that"
}

def _tokenize(text: str):
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9áéíóúñü\s]", " ", text)
    tokens = [t for t in text.split() if t and t not in _STOPWORDS and len(t) > 2]
    return tokens

def _build_tfidf_docs(docs: List[str]):
    N = len(docs)
    doc_terms = []
    df = {}
    for doc in docs:
        toks = _tokenize(doc)
        tf = {}
        for t in toks:
            tf[t] = tf.get(t, 0) + 1
        doc_terms.append(tf)
        for t in set(toks):
            df[t] = df.get(t, 0) + 1
    idf = {}
    for t, f in df.items():
        idf[t] = math.log((N + 1) / (f + 1)) + 1.0
    vocab = list(df.keys())
    return doc_terms, idf, vocab

def _vec_from_tf(tf: dict, idf: dict):
    vec = {}
    for t, cnt in tf.items():
        if t in idf:
            vec[t] = cnt * idf[t]
    return vec

def _cosine_similarity(v1: dict, v2: dict) -> float:
    if not v1 or not v2:
        return 0.0
    dot = 0.0
    for k, v in v1.items():
        if k in v2:
            dot += v * v2[k]
    norm1 = math.sqrt(sum(v*v for v in v1.values()))
    norm2 = math.sqrt(sum(v*v for v in v2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

def _init_ai_index(movies_list):
    docs = [ (m.descripcion or "") for m in movies_list ]
    doc_terms, idf, vocab = _build_tfidf_docs(docs)
    vectors = []
    for tf in doc_terms:
        vectors.append(_vec_from_tf(tf, idf))
    id_to_index = { m.id: idx for idx, m in enumerate(movies_list) }
    return {
        "idf": idf,
        "vocab": vocab,
        "doc_terms": doc_terms,
        "vectors": vectors,
        "id_to_index": id_to_index,
        "movies_snapshot": [ { "id": m.id, "titulo": m.titulo } for m in movies_list ]
    }

# Inicializar índice AI con la lista 'movies' (asegúrate que 'movies' existe)
_AI_INDEX = _init_ai_index(movies)

# función util para recalcular (llamar después de cambios CRUD)
def _rebuild_ai_index():
    global _AI_INDEX
    _AI_INDEX = _init_ai_index(movies)

# Endpoints AI
from fastapi import Query

@app.get("/ai/recommendations/{movie_id}", summary="Recomendar películas similares por descripción")
def ai_recommendations(movie_id: int, n: int = Query(3, ge=1, le=20)):
    idx_map = _AI_INDEX["id_to_index"]
    if movie_id not in idx_map:
        raise HTTPException(status_code=404, detail="Película no encontrada para recomendaciones")
    idx = idx_map[movie_id]
    target_vec = _AI_INDEX["vectors"][idx]
    scores = []
    for i, vec in enumerate(_AI_INDEX["vectors"]):
        if i == idx:
            continue
        score = _cosine_similarity(target_vec, vec)
        scores.append( (i, score) )
    scores.sort(key=lambda x: x[1], reverse=True)
    results = []
    for i, sc in scores[:n]:
        movie = movies[i]
        results.append({"id": movie.id, "titulo": movie.titulo, "score": round(sc, 4)})
    return results

@app.get("/ai/keywords/{movie_id}", summary="Extraer keywords por TF-IDF de la descripción")
def ai_keywords(movie_id: int, k: int = Query(5, ge=1, le=30)):
    idx_map = _AI_INDEX["id_to_index"]
    if movie_id not in idx_map:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    idx = idx_map[movie_id]
    tf = _AI_INDEX["doc_terms"][idx]
    idf = _AI_INDEX["idf"]
    tfidf = { t: (cnt * idf.get(t, 0.0)) for t, cnt in tf.items() }
    sorted_terms = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)
    topk = [ t for t, score in sorted_terms[:k] ]
    return {"movie_id": movie_id, "keywords": topk}


