# -*- coding: utf-8 -*-
"""
Emergency Assistance Agent
"""
from app.agents.base_agent import BaseAgent
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class EmergencyAgent(BaseAgent):
    """Agent for emergency situations"""
    
    def __init__(self):
        super().__init__(
            name="Emergency Agent",
            description="Provides emergency assistance and contact information"
        )
        
        self.emergency_contacts = {
            "police": {
                "number": "911",
                "name": "Polisi",
                "description": "Untuk kejahatan, kehilangan"
            },
            "ambulance": {
                "number": "997",
                "name": "Ambulans",
                "description": "Untuk keadaan darurat medis"
            },
            "fire": {
                "number": "998",
                "name": "Pemadam Kebakaran",
                "description": "Untuk kebakaran"
            },
            "traffic": {
                "number": "993",
                "name": "Lalu Lintas",
                "description": "Untuk kecelakaan lalu lintas"
            },
            "electricity": {
                "number": "933",
                "name": "Listrik Darurat",
                "description": "Untuk masalah listrik"
            },
            "consulate_indo": {
                "number": "+966 12 667 0080",
                "name": "KJRI Jeddah",
                "description": "Untuk WNI yang membutuhkan bantuan"
            }
        }
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle emergency situations"""
        try:
            query = input_data.get("query", "").lower()
            emergency_type = input_data.get("type", "general")
            
            # Detect emergency type
            if any(word in query for word in ['sakit', 'medis', 'rumah sakit', 'ambulans']):
                return self._medical_emergency()
            elif any(word in query for word in ['hilang', 'paspor', 'dompet', 'polisi']):
                return self._lost_items_emergency()
            elif any(word in query for word in ['tersesat', 'lost', 'tidak tahu']):
                return self._lost_location_emergency()
            else:
                return self._general_emergency_info()
                
        except Exception as e:
            logger.error(f"Error in EmergencyAgent: {e}")
            return {
                "agent": self.name,
                "response": self._critical_emergency_response()
            }
    
    def _medical_emergency(self) -> Dict[str, Any]:
        """Medical emergency response"""
        response = """
🚨 *DARURAT MEDIS*

*LANGKAH CEPAT:*
1. Hubungi ambulans: *997*
2. Atau telpon hotel untuk ambulans
3. Jelaskan kondisi dalam bahasa sederhana

*RUMAH SAKIT TERDEKAT:*
- Ajyad Hospital (5 min dari Haram)
  📞 +966 12 549 8000
- King Abdullah Medical City
  📞 +966 12 549 5555
- Al Noor Specialist Hospital
  📞 +966 12 667 5555

*APOTEK 24 JAM:*
- Nahdi Pharmacy (Abraj Al Bait Mall)
- Al Dawaa Pharmacy

*TIPS:*
- Bawa kartu BPJS/asuransi
- Catat nama obat dalam bahasa Inggris
- Minta resep tertulis

🇮🇩 *Bantuan WNI:*
KJRI Jeddah: +966 12 667 0080
        """
        
        return {
            "agent": self.name,
            "response": response.strip(),
            "priority": "critical"
        }
    
    def _lost_items_emergency(self) -> Dict[str, Any]:
        """Lost items emergency"""
        response = """
🔍 *KEHILANGAN BARANG*

*PASPOR/DOKUMEN HILANG:*
1. Lapor hotel segera
2. Lapor polisi terdekat (911)
3. Hubungi KJRI Jeddah:
   📞 +966 12 667 0080
   📱 Emergency: +966 50 521 5066

*DOMPET/UANG HILANG:*
1. Cek lost & found Masjidil Haram
   📍 Basement level
2. Lapor hotel security
3. Block kartu ATM/credit card
4. Hubungi bank Indonesia

*BARANG HILANG DI HARAM:*
- Lost & Found: Basement Masjidil Haram
- Waktu operasional: 24 jam
- Bawa ID untuk klaim

*HP HILANG:*
- Track via Find My Phone
- Lapor polisi dengan IMEI
- Block SIM card

💡 *Pencegahan:*
- Fotokopi paspor (simpan terpisah)
- Catat nomor darurat di kertas
- Gunakan money belt
- Jangan bawa barang berharga saat thawaf
        """
        
        return {
            "agent": self.name,
            "response": response.strip(),
            "priority": "high"
        }
    
    def _lost_location_emergency(self) -> Dict[str, Any]:
        """Lost location emergency"""
        response = """
📍 *TERSESAT / LOST*

*LANGKAH TENANG:*
1. Jangan panik!
2. Tetap di tempat ramai
3. Tanyakan petugas/security

*JIKA DI MASJIDIL HARAM:*
- Cari info desk terdekat
- Tanya jamaah Indonesia
- Lihat papan petunjuk (ada bahasa Indonesia)
- Gunakan landmark: pintu terdekat

*JIKA DI LUAR:*
- Tunjukkan alamat hotel ke taxi
- Sebut nama landmark terkenal
- Gunakan Google Maps
- Telpon hotel minta dijemput

*KONTAK PENTING:*
- Hotel: [Simpan nomor hotel]
- Travel: [Simpan nomor tour guide]
- KJRI: +966 12 667 0080

*BAHASA SURVIVAL:*
- "Ayna al-funduq?" = Di mana hotel?
- "Urid al-masjid" = Saya mau ke masjid
- "Sa'idni" = Tolong saya

💡 *Tips:*
- Screenshot peta hotel
- Simpan kartu nama hotel
- Bawa foto landmark hotel
- Selalu charge HP
        """
        
        return {
            "agent": self.name,
            "response": response.strip(),
            "priority": "medium"
        }
    
    def _general_emergency_info(self) -> Dict[str, Any]:
        """General emergency information"""
        response = """
🆘 *KONTAK DARURAT SAUDI ARABIA*

*EMERGENCY SERVICES:*
- Polisi: *911*
- Ambulans: *997*
- Pemadam Kebakaran: *998*
- Lalu Lintas: *993*

*KONSULAT INDONESIA:*
🇮🇩 KJRI Jeddah
- Telpon: +966 12 667 0080
- Emergency 24/7: +966 50 521 5066
- Email: konsuler.jed@kemlu.go.id

*KONDISI DARURAT:*
- Sakit: /emergency medis
- Kehilangan: /emergency hilang
- Tersesat: /emergency tersesat

*INFORMASI PENTING:*
- Simpan nomor ini di HP
- Catat di kertas (backup)
- Beritahu keluarga
- Share location real-time ke keluarga

*TRAVEL AGENT:*
[Hubungi travel agent Anda]

💡 *Tetap tenang dan berdoa!*
Allah selalu bersama orang yang sabar.
        """
        
        return {
            "agent": self.name,
            "response": response.strip(),
            "priority": "info"
        }
    
    def _critical_emergency_response(self) -> str:
        """Critical emergency fallback"""
        return """
🚨 *DARURAT!*

Hubungi SEGERA:
- Ambulans: *997*
- Polisi: *911*
- KJRI Jeddah: +966 12 667 0080

Atau minta bantuan orang terdekat!
        """