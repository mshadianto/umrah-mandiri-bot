# -*- coding: utf-8 -*-
"""
Seed knowledge base with umrah content
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.rag.vector_store import VectorStore
from backend.app.rag.embeddings import EmbeddingService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Knowledge base content
UMRAH_KNOWLEDGE = [
    # Manasik
    {
        "text": """Rukun Umrah ada 4: 
1. Ihram - niat dan memakai pakaian ihram dari miqat
2. Thawaf - mengelilingi Ka'bah 7 kali
3. Sa'i - berjalan antara Safa dan Marwa 7 kali
4. Tahalul - mencukur atau menggunting rambut

Jika salah satu rukun tidak dilakukan, umrah tidak sah.""",
        "category": "manasik",
        "source": "Fiqih Sunnah - Sayyid Sabiq",
        "topic": "rukun_umrah"
    },
    {
        "text": """Tata cara ihram:
1. Mandi sunnah
2. Pakai pakaian ihram (laki-laki: 2 kain putih tanpa jahitan, perempuan: pakaian biasa menutup aurat)
3. Wangi-wangian sebelum niat (sunnah)
4. Sholat sunnah ihram 2 rakaat
5. Niat umrah: Labbaika Allahumma 'umratan
6. Ucapkan talbiyah""",
        "category": "manasik",
        "source": "Panduan Umrah - Syaikh Bin Baz",
        "topic": "ihram"
    },
    {
        "text": """Tata cara thawaf:
1. Mulai dari garis Hajar Aswad
2. Istilam (cium/tunjuk) Hajar Aswad sambil takbir
3. Thawaf 7 putaran berlawanan arah jarum jam
4. Ka'bah harus di sebelah kiri
5. Hijr Ismail harus dilalui (di luar)
6. Ramal pada 3 putaran pertama (laki-laki)
7. Sentuh/tunjuk Rukun Yamani
8. Berdoa antara Rukun Yamani dan Hajar Aswad
9. Sholat 2 rakaat di belakang Maqam Ibrahim""",
        "category": "manasik",
        "source": "Minhajul Muslim",
        "topic": "thawaf"
    },
    {
        "text": """Tata cara sa'i:
1. Mulai dari bukit Safa
2. Hadap Ka'bah, takbir dan tahlil 3x
3. Jalan menuju Marwa
4. Lari kecil di area lampu hijau (laki-laki)
5. Sampai Marwa, hadap Ka'bah, takbir dan tahlil
6. Kembali ke Safa untuk putaran ke-2
7. Total 7 kali, berakhir di Marwa""",
        "category": "manasik",
        "source": "Fiqih Sunnah",
        "topic": "sai"
    },
    
    # Doa
    {
        "text": """Talbiyah:
لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيْكَ لَكَ لَبَّيْكَ
إِنَّ الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ لَا شَرِيْكَ لَكَ

Labbaika Allahumma labbaik, labbaika la syarika laka labbaik
Innal hamda wan ni'mata laka wal mulk, la syarika lak

Artinya: Aku penuhi panggilan-Mu ya Allah, aku penuhi panggilan-Mu. Aku penuhi panggilan-Mu, tidak ada sekutu bagi-Mu, aku penuhi panggilan-Mu. Sesungguhnya segala puji, nikmat, dan kerajaan adalah milik-Mu, tidak ada sekutu bagi-Mu.""",
        "category": "doa",
        "source": "Shahih Bukhari & Muslim",
        "topic": "talbiyah"
    },
    {
        "text": """Doa istilam Hajar Aswad:
بِسْمِ اللهِ وَاللهُ أَكْبَرُ

Bismillahi wallahu akbar

Artinya: Dengan nama Allah, Allah Maha Besar""",
        "category": "doa",
        "source": "Hisnul Muslim",
        "topic": "doa_hajar_aswad"
    },
    {
        "text": """Doa antara Rukun Yamani dan Hajar Aswad:
رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ

Rabbana atina fid dunya hasanah wa fil akhirati hasanah wa qina 'adzaban nar

Artinya: Ya Tuhan kami, berilah kami kebaikan di dunia dan kebaikan di akhirat, dan lindungilah kami dari azab neraka.

Sumber: QS. Al-Baqarah: 201""",
        "category": "doa",
        "source": "Al-Quran",
        "topic": "doa_thawaf"
    },
    {
        "text": """Doa minum zamzam:
اللَّهُمَّ إِنِّي أَسْأَلُكَ عِلْمًا نَافِعًا وَرِزْقًا وَاسِعًا وَشِفَاءً مِنْ كُلِّ دَاءٍ

Allahumma inni as'aluka 'ilman nafi'a wa rizqan wasi'a wa syifa'an min kulli da'

Artinya: Ya Allah, aku memohon kepada-Mu ilmu yang bermanfaat, rezeki yang luas, dan kesembuhan dari segala penyakit.

Hadits: Air zamzam adalah untuk apa yang diniatkan (HR. Ahmad, Ibnu Majah)""",
        "category": "doa",
        "source": "Hadits Ahmad",
        "topic": "doa_zamzam"
    },
    
    # Tips praktis
    {
        "text": """Tips thawaf:
- Waktu terbaik: setelah sholat subuh (sepi)
- Hindari waktu ramai: setelah Maghrib dan Isya
- Thawaf di lantai atas lebih longgar
- Jika ramai, tidak perlu istilam Hajar Aswad, cukup tunjuk dari jauh
- Gunakan tongsis untuk foto, jangan menghalangi jamaah lain
- Perhatikan orang tua dan anak-anak""",
        "category": "tips",
        "source": "Pengalaman Jamaah",
        "topic": "tips_thawaf"
    },
    {
        "text": """Larangan saat ihram:
1. Memakai pakaian berjahit (laki-laki)
2. Menutup kepala (laki-laki)
3. Memakai wewangian
4. Memotong kuku atau rambut
5. Berburu atau membunuh binatang
6. Hubungan suami istri
7. Khitbah (melamar)
8. Akad nikah

Dam (denda) jika melanggar: sembelih kambing atau puasa 3 hari""",
        "category": "manasik",
        "source": "Fiqih Umrah",
        "topic": "larangan_ihram"
    }
]

async def seed_knowledge():
    """Seed knowledge base"""
    try:
        logger.info("🌱 Starting knowledge base seeding...")
        
        # Initialize services
        vector_store = VectorStore()
        embeddings_service = EmbeddingService()
        
        # Create collection
        vector_store.create_collection()
        logger.info("✅ Collection ready")
        
        # Prepare data
        texts = [item["text"] for item in UMRAH_KNOWLEDGE]
        metadatas = [
            {
                "category": item["category"],
                "source": item["source"],
                "topic": item["topic"]
            }
            for item in UMRAH_KNOWLEDGE
        ]
        
        # Generate embeddings
        logger.info("🔄 Generating embeddings...")
        embedding_vectors = await embeddings_service.embed_texts(texts)
        logger.info(f"✅ Generated {len(embedding_vectors)} embeddings")
        
        # Add to vector store
        logger.info("🔄 Adding documents to vector store...")
        await vector_store.add_documents(
            texts=texts,
            embeddings=embedding_vectors,
            metadatas=metadatas
        )
        
        logger.info(f"✅ Seeded {len(texts)} documents successfully!")
        logger.info("🎉 Knowledge base ready!")
        
    except Exception as e:
        logger.error(f"❌ Error seeding knowledge: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(seed_knowledge())