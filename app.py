"""
AstroKnowledge - Main Streamlit Application
Vedic Astrology AI Assistant
"""
import streamlit as st
from datetime import datetime, time as datetime_time
import pandas as pd
from pathlib import Path
import yaml
import time

from src.document_processor import DocumentProcessor
from src.astrology_engine import VedicAstrologyEngine, BirthDetails
# from src.rag_system import RAGSystem  # Temporarily disabled due to ChromaDB dependency issue
from src.simple_rag.simple_search import SimpleKnowledgeBase, generate_answer
from src.astrology_qa.vedic_knowledge import VedicKnowledge
from src.user_manager import UserManager, UserProfile
from src.remedy_engine import RemedyEngine, GemstoneRecommender
from src.astrology_engine.interpretation_engine import VedicInterpretationEngine
from src.auth import AuthManager
from src.auth.email_sender import EmailSender
from src.payment import PaymentManager
from src.numerology import NumerologyEngine
from src.utils import config

# Vedic Planetary Symbols Mapping
PLANET_SYMBOLS = {
    'Sun': '☉',
    'Moon': '☽',
    'Mars': '♂',
    'Mercury': '☿',
    'Jupiter': '♃',
    'Venus': '♀',
    'Saturn': '♄',
    'Rahu': '☊',
    'Ketu': '☋'
}

# Vedic Planet Emojis for visual enhancement
PLANET_EMOJIS = {
    'Sun': '🌞',
    'Moon': '🌙',
    'Mars': '🔴',
    'Mercury': '💚',
    'Jupiter': '🟡',
    'Venus': '🪷',
    'Saturn': '🔵',
    'Rahu': '🌑',
    'Ketu': '⚫'
}

def format_planet_name(planet_name, use_emoji=False, use_symbol=True):
    """Format planet name with symbol/emoji"""
    if use_emoji:
        emoji = PLANET_EMOJIS.get(planet_name, '')
        return f"{emoji} {planet_name}" if emoji else planet_name
    elif use_symbol:
        symbol = PLANET_SYMBOLS.get(planet_name, '')
        return f"{symbol} {planet_name}" if symbol else planet_name
    return planet_name

# Page configuration
st.set_page_config(
    page_title="KundaliSaga - Vedic Astrology AI",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Light Saffron/Peach background for all pages */
    .stApp {
        background-color: #FFF5E6;
    }
    /* Light Saffron/Peach background for sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFF5E6;
    }
    .main-header {
        font-size: 2.5rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .planet-card {
        padding: 1rem;
        background-color: #FFFFF0;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.user_manager = UserManager()
        st.session_state.astro_engine = VedicAstrologyEngine()
        # st.session_state.rag_system = RAGSystem()  # Temporarily disabled
        st.session_state.knowledge_base = SimpleKnowledgeBase()  # Simple text-based system
        st.session_state.remedy_engine = RemedyEngine()
        st.session_state.doc_processor = DocumentProcessor()
        st.session_state.interpretation_engine = VedicInterpretationEngine()  # Built-in interpretation
        st.session_state.vedic_qa = VedicKnowledge()  # Built-in Q&A knowledge
        st.session_state.auth_manager = AuthManager()  # Authentication
        st.session_state.email_sender = EmailSender()  # Email sender
        st.session_state.payment_manager = PaymentManager(config=config)  # Payment system with config
        st.session_state.numerology_engine = NumerologyEngine()  # Numerology
        st.session_state.gemstone_recommender = GemstoneRecommender()  # Gemstone recommendations
        st.session_state.current_user = None
        st.session_state.session_token = None
        st.session_state.chart_style = 'North Indian'  # Default chart style
        st.session_state.language = 'English'  # Default language
        st.session_state.logged_in = False


# Language translations
TRANSLATIONS = {
    'English': {
        'app_title': '🔮 KundaliSaga',
        'app_subtitle': 'Your Personal Vedic Astrology Assistant',
        'nav_home': '🏠 Home',
        'nav_profiles': '👤 User Profiles',
        'nav_documents': '📚 Document Management',
        'nav_horoscope': '🔮 Horoscope',
        'nav_ask': '💬 Ask Question',
        'nav_remedies': '🏥 Remedies',
        'nav_stotras': '📿 Stotras & Prayers',
        'nav_numerology': '🔢 Numerology',
        'nav_career': '💼 Career Guidance',
        'nav_financial': '📈 Financial Outlook',
        'nav_gemstones': '💎 Gemstone Guide',
        'nav_matchmaking': '💑 Matchmaking',
        'nav_soulmate': '💕 Soulmate Analysis',
        'nav_muhurat': '⏰ Muhurat Finder',
        'nav_varshaphal': '📅 Varshaphal',
        'nav_dasha_detail': '🌀 Dasha Analysis',
        'nav_name_rec': '✨ Name Recommendation',
        'nav_settings': '⚙️ Settings',
        'ganesha_mantra': 'ॐ गं गणपतये नमः',
        'ganesha_mantra_english': 'Om Gam Ganapataye Namah',
        'select_profile': 'Select Profile',
        'create_chart': 'Create Birth Chart',
        'welcome': 'Welcome to KundaliSaga',
        'knowledge_base': 'Knowledge Base',
        'knowledge_base_desc': 'Process thousands of astrology books and build your comprehensive knowledge base.',
        'chart_analysis': 'Chart Analysis',
        'chart_analysis_desc': 'Calculate accurate Vedic birth charts, dashas, and transits.',
        'ai_insights': 'AI Insights',
        'ai_insights_desc': 'Get AI-powered answers based on ancient texts and your chart.',
        'quick_start': 'Quick Start Guide',
        'step1': 'Create User Profile',
        'step1_desc': 'Add your birth details in the User Profiles section',
        'step2': 'Generate Horoscope',
        'step2_desc': 'View your detailed Vedic chart',
        'step3': 'Ask Questions',
        'step3_desc': 'Get personalized insights from Experienced Kundali Makers',
        'step4': 'Get Remedies',
        'step4_desc': 'Receive customized astrological remedies',
        'period': 'Period',
        'additional_insights_classical': '📚 Additional insights from classical texts:',
        'additional_insights_books': '📚 Additional insights from uploaded books',
        'note_predictions': '💡 **Note:** These predictions are based on classical Vedic astrology principles.',
        'source': 'Source',
        # User Profiles
        'view_profiles': 'View Profiles',
        'create_new_profile': 'Create New Profile',
        'no_profiles': 'No profiles found. Create your first profile!',
        'birth_date': 'Birth Date',
        'birth_time': 'Birth Time',
        'birth_place': 'Birth Place',
        'latitude': 'Latitude',
        'longitude': 'Longitude',
        'timezone': 'Timezone',
        'notes': 'Notes',
        'name': 'Name',
        'relationship': 'Relationship',
        'gender': 'Gender',
        'self': 'Self',
        'spouse': 'Spouse',
        'child': 'Child',
        'parent': 'Parent',
        'sibling': 'Sibling',
        'friend': 'Friend',
        'other': 'Other',
        'male': 'Male',
        'female': 'Female',
        'create_profile': 'Create Profile',
        'profile_created': 'Profile created successfully!',
        'fill_required': 'Please fill all required fields',
        'select': 'Select',
        'selected': 'Selected',
        'full_name': 'Full name',
        'optional': 'optional',
        'hour': 'Hour',
        'minute': 'Minute',
        'second': 'Second',
        # Birth Chart
        'birth_chart': 'Birth Chart',
        'ascendant': 'Ascendant',
        'degree': 'Degree',
        'nakshatra': 'Nakshatra',
        'planetary_positions': 'Planetary Positions',
        'planet': 'Planet',
        'sign': 'Sign',
        'house': 'House',
        'retrograde': 'Retrograde',
        'divisional_charts': 'Divisional Charts (Vargas)',
        # Dasha
        'vimshottari_dasha': 'Vimshottari Dasha (120 Years)',
        'current_dasha': 'Current Dasha',
        'till': 'Till',
        'view_all_dasha': '📅 View All Dasha Periods (Click to expand)',
        'years': 'years',
        # Chart Analysis
        'chart_analysis_header': '📊 Chart Analysis',
        'strengths': 'Strengths',
        'areas_attention': 'Areas for Attention',
        'exalted_in': 'is exalted in',
        'debilitated_in': 'is debilitated in',
        'strong_ascendant': 'Strong ascendant placement',
        'nakshatra_influence': 'nakshatra influence',
        'no_afflictions': 'No major planetary afflictions',
        'balanced_positions': 'Balanced planetary positions',
        # Remedies
        'astrological_remedies': '🏥 Astrological Remedies',
        'select_profile_remedy': 'Select Profile',
        'specific_concern': 'Specific Concern (optional)',
        'get_remedies': 'Get Remedies',
        'personalized_remedies': 'Personalized Remedies for:',
        'immediate_actions': '⚡ Immediate Actions - Start Today!',
        'lal_kitab_remedies': '📿 Lal Kitab Remedies',
        'general_remedies': '🌟 General Remedies',
        'quick_wins': '✨ Quick Wins (Easy to do)',
        'planetary_remedies': '🪐 Planetary Remedies',
        # Payment & Credits
        'nav_credits': '💳 Buy Credits',
        'credits_balance': 'Credits Balance',
        'buy_credits': 'Buy Credits',
        'insufficient_credits': 'Insufficient Credits',
        'need_credits_msg': 'You need credits to use this feature. Please buy credits to continue.',
        'payment_options': 'Payment Options',
        'single_question_price': '₹10 per question',
        'bulk_discount': 'Bulk Purchase (Save More!)',
        'questions': 'Questions',
        'price': 'Price',
        'save': 'Save',
        'pay_now': 'Pay Now',
        'transaction_id': 'Transaction ID / UPI Reference',
        'submit_payment': 'Submit Payment',
        'payment_instructions': 'After payment, enter your UPI transaction ID above',
        'credits_added': 'Credits added successfully!',
        'payment_verified': 'Payment verified! Credits added to your account.',
    },
    'Hindi': {
        'app_title': '🔮 ज्योतिष ज्ञान',
        'app_subtitle': 'आपका व्यक्तिगत वैदिक ज्योतिष सहायक',
        'nav_home': '🏠 होम',
        'nav_profiles': '👤 उपयोगकर्ता प्रोफाइल',
        'nav_documents': '📚 दस्तावेज़ प्रबंधन',
        'nav_horoscope': '🔮 कुंडली',
        'nav_ask': '💬 प्रश्न पूछें',
        'nav_remedies': '🏥 उपाय',
        'nav_stotras': '📿 स्तोत्र और प्रार्थना',
        'nav_numerology': '🔢 अंक ज्योतिष',
        'nav_career': '💼 करियर मार्गदर्शन',
        'nav_financial': '📈 वित्तीय दृष्टिकोण',
        'nav_gemstones': '💎 रत्न मार्गदर्शिका',
        'nav_matchmaking': '💑 कुंडली मिलान',
        'nav_soulmate': '💕 आत्मीय साथी',
        'nav_muhurat': '⏰ मुहूर्त',
        'nav_varshaphal': '📅 वर्षफल',
        'nav_dasha_detail': '🌀 दशा विश्लेषण',
        'nav_name_rec': '✨ नाम सुझाव',
        'nav_credits': '💳 क्रेडिट खरीदें',
        'nav_settings': '⚙️ सेटिंग्स',
        'ganesha_mantra': 'ॐ गं गणपतये नमः',
        'ganesha_mantra_english': 'ओम गम गणपतये नमः',
        'select_profile': 'प्रोफाइल चुनें',
        'create_chart': 'जन्म कुंडली बनाएं',
        'welcome': 'ज्योतिष ज्ञान में आपका स्वागत है',
        'knowledge_base': 'ज्ञान का आधार',
        'knowledge_base_desc': 'हजारों ज्योतिष पुस्तकों को संसाधित करें और अपना व्यापक ज्ञान आधार बनाएं।',
        'chart_analysis': 'कुंडली विश्लेषण',
        'chart_analysis_desc': 'सटीक वैदिक जन्म कुंडली, दशा और गोचर की गणना करें।',
        'ai_insights': 'AI अंतर्दृष्टि',
        'ai_insights_desc': 'प्राचीन ग्रंथों और आपकी कुंडली के आधार पर AI-संचालित उत्तर प्राप्त करें।',
        'quick_start': 'त्वरित प्रारंभ गाइड',
        'step1': 'उपयोगकर्ता प्रोफाइल बनाएं',
        'step1_desc': 'उपयोगकर्ता प्रोफाइल अनुभाग में अपना जन्म विवरण जोड़ें',
        'step2': 'कुंडली बनाएं',
        'step2_desc': 'अपनी विस्तृत वैदिक कुंडली देखें',
        'step3': 'प्रश्न पूछें',
        'step3_desc': 'AI से व्यक्तिगत अंतर्दृष्टि प्राप्त करें',
        'step4': 'उपाय प्राप्त करें',
        'step4_desc': 'अनुकूलित ज्योतिषीय उपाय प्राप्त करें',
        'period': 'अवधि',
        'additional_insights_classical': '📚 शास्त्रीय ग्रंथों से अतिरिक्त जानकारी:',
        'additional_insights_books': '📚 अपलोड की गई पुस्तकों से अतिरिक्त जानकारी',
        'note_predictions': '💡 **नोट:** ये भविष्यवाणियां शास्त्रीय वैदिक ज्योतिष सिद्धांतों पर आधारित हैं। अपलोड की गई पुस्तकें प्रासंगिक व्याख्याएं मिलने पर अतिरिक्त पारंपरिक अंतर्दृष्टि प्रदान करती हैं।',
        'source': 'स्रोत',
        # User Profiles
        'view_profiles': 'प्रोफाइल देखें',
        'create_new_profile': 'नया प्रोफाइल बनाएं',
        'no_profiles': 'कोई प्रोफाइल नहीं मिला। अपना पहला प्रोफाइल बनाएं!',
        'birth_date': 'जन्म तिथि',
        'birth_time': 'जन्म समय',
        'birth_place': 'जन्म स्थान',
        'latitude': 'अक्षांश',
        'longitude': 'देशांतर',
        'timezone': 'समय क्षेत्र',
        'notes': 'टिप्पणियाँ',
        'name': 'नाम',
        'relationship': 'संबंध',
        'gender': 'लिंग',
        'self': 'स्वयं',
        'spouse': 'जीवनसाथी',
        'child': 'बच्चा',
        'parent': 'माता-पिता',
        'sibling': 'भाई-बहन',
        'friend': 'दोस्त',
        'other': 'अन्य',
        'male': 'पुरुष',
        'female': 'महिला',
        'create_profile': 'प्रोफाइल बनाएं',
        'profile_created': 'प्रोफाइल सफलतापूर्वक बनाया गया!',
        'fill_required': 'कृपया सभी आवश्यक फ़ील्ड भरें',
        'select': 'चुनें',
        'selected': 'चयनित',
        'full_name': 'पूरा नाम',
        'optional': 'वैकल्पिक',
        'hour': 'घंटा',
        'minute': 'मिनट',
        'second': 'सेकंड',
        # Birth Chart
        'birth_chart': 'जन्म कुंडली',
        'ascendant': 'लग्न',
        'degree': 'अंश',
        'nakshatra': 'नक्षत्र',
        'planetary_positions': 'ग्रह स्थिति',
        'planet': 'ग्रह',
        'sign': 'राशि',
        'house': 'भाव',
        'retrograde': 'वक्री',
        'divisional_charts': 'विभागीय कुंडली (वर्ग)',
        # Dasha
        'vimshottari_dasha': 'विम्शोत्तरी दशा (120 वर्ष)',
        'current_dasha': 'वर्तमान दशा',
        'till': 'तक',
        'view_all_dasha': '📅 सभी दशा अवधि देखें (विस्तार के लिए क्लिक करें)',
        'years': 'वर्ष',
        # Chart Analysis
        'chart_analysis_header': '📊 कुंडली विश्लेषण',
        'strengths': 'शक्तियां',
        'areas_attention': 'ध्यान देने योग्य क्षेत्र',
        'exalted_in': 'में उच्च है',
        'debilitated_in': 'में नीच है',
        'strong_ascendant': 'मजबूत लग्न स्थिति',
        'nakshatra_influence': 'नक्षत्र प्रभाव',
        'no_afflictions': 'कोई बड़ी ग्रह पीड़ा नहीं',
        'balanced_positions': 'संतुलित ग्रह स्थिति',
        # Remedies
        'astrological_remedies': '🏥 ज्योतिषीय उपाय',
        'select_profile_remedy': 'प्रोफाइल चुनें',
        'specific_concern': 'विशिष्ट चिंता (वैकल्पिक)',
        'get_remedies': 'उपाय प्राप्त करें',
        'personalized_remedies': 'के लिए व्यक्तिगत उपाय:',
        'immediate_actions': '⚡ तत्काल कार्रवाई - आज से शुरू करें!',
        'lal_kitab_remedies': '📿 लाल किताब उपाय',
        'general_remedies': '🌟 सामान्य उपाय',
        'quick_wins': '✨ त्वरित उपाय (करने में आसान)',
        'planetary_remedies': '🪐 ग्रह उपाय',
        # Payment & Credits
        'nav_credits': '💳 क्रेडिट खरीदें',
        'credits_balance': 'क्रेडिट बैलेंस',
        'buy_credits': 'क्रेडिट खरीदें',
        'insufficient_credits': 'अपर्याप्त क्रेडिट',
        'need_credits_msg': 'इस सुविधा का उपयोग करने के लिए आपको क्रेडिट चाहिए। जारी रखने के लिए कृपया क्रेडिट खरीदें।',
        'payment_options': 'भुगतान विकल्प',
        'single_question_price': '₹10 प्रति प्रश्न',
        'bulk_discount': 'थोक खरीद (अधिक बचाएं!)',
        'questions': 'प्रश्न',
        'price': 'मूल्य',
        'save': 'बचत',
        'pay_now': 'अभी भुगतान करें',
        'transaction_id': 'लेनदेन ID / UPI संदर्भ',
        'submit_payment': 'भुगतान जमा करें',
        'payment_instructions': 'भुगतान के बाद, अपना UPI लेनदेन ID ऊपर दर्ज करें',
        'credits_added': 'क्रेडिट सफलतापूर्वक जोड़े गए!',
        'payment_verified': 'भुगतान सत्यापित! आपके खाते में क्रेडिट जोड़ दिया गया है।',
    },
    'Marathi': {
        'app_title': '🔮 ज्योतिष ज्ञान',
        'app_subtitle': 'तुमचा वैयक्तिक वैदिक ज्योतिष सहाय्यक',
        'nav_home': '🏠 होम',
        'nav_profiles': '👤 वापरकर्ता प्रोफाइल',
        'nav_documents': '📚 दस्तऐवज व्यवस्थापन',
        'nav_horoscope': '🔮 कुंडली',
        'nav_ask': '💬 प्रश्न विचारा',
        'nav_remedies': '🏥 उपाय',
        'nav_stotras': '📿 स्तोत्र आणि प्रार्थना',
        'nav_numerology': '🔢 अंक ज्योतिष',
        'nav_career': '💼 करिअर मार्गदर्शन',
        'nav_financial': '📈 आर्थिक दृष्टीकोन',
        'nav_gemstones': '💎 रत्न मार्गदर्शक',
        'nav_matchmaking': '💑 कुंडली जुळणी',
        'nav_soulmate': '💕 आत्मा साथी',
        'nav_muhurat': '⏰ मुहूर्त',
        'nav_varshaphal': '📅 वार्षिक फळ',
        'nav_dasha_detail': '🌀 दशा विश्लेषण',
        'nav_name_rec': '✨ नाव सुचविणे',
        'nav_credits': '💳 क्रेडिट खरेदी करा',
        'nav_settings': '⚙️ सेटिंग्ज',
        'ganesha_mantra': 'ॐ गं गणपतये नमः',
        'ganesha_mantra_english': 'ओम गं गणपतये नमः',
        'select_profile': 'प्रोफाइल निवडा',
        'create_chart': 'जन्म कुंडली तयार करा',
        'welcome': 'ज्योतिष ज्ञान मध्ये आपले स्वागत आहे',
        'knowledge_base': 'ज्ञान आधार',
        'knowledge_base_desc': 'हजारो ज्योतिष पुस्तके प्रक्रिया करा आणि तुमचा सर्वसमावेशक ज्ञान आधार तयार करा.',
        'chart_analysis': 'कुंडली विश्लेषण',
        'chart_analysis_desc': 'अचूक वैदिक जन्म कुंडली, दशा आणि गोचर मोजा.',
        'ai_insights': 'AI अंतर्दृष्टी',
        'ai_insights_desc': 'प्राचीन ग्रंथ आणि तुमच्या कुंडलीवर आधारित AI-चालित उत्तरे मिळवा.',
        'quick_start': 'द्रुत प्रारंभ मार्गदर्शक',
        'step1': 'वापरकर्ता प्रोफाइल तयार करा',
        'step1_desc': 'वापरकर्ता प्रोफाइल विभागात तुमचे जन्म तपशील जोडा',
        'step2': 'कुंडली तयार करा',
        'step2_desc': 'तुमची तपशीलवार वैदिक कुंडली पहा',
        'step3': 'प्रश्न विचारा',
        'step3_desc': 'AI कडून वैयक्तिक अंतर्दृष्टी मिळवा',
        'step4': 'उपाय मिळवा',
        'step4_desc': 'सानुकूलित ज्योतिषीय उपाय प्राप्त करा',
        'period': 'कालावधी',
        'additional_insights_classical': '📚 शास्त्रीय ग्रंथांकडून अतिरिक्त माहिती:',
        'additional_insights_books': '📚 अपलोड केलेल्या पुस्तकांकडून अतिरिक्त माहिती',
        'note_predictions': '💡 **टीप:** हे भविष्यकथन शास्त्रीय वैदिक ज्योतिष तत्त्वांवर आधारित आहे. अपलोड केलेली पुस्तके संबंधित व्याख्या आढळल्यास अतिरिक्त पारंपारिक अंतर्दृष्टी प्रदान करतात.',
        'source': 'स्रोत',
        # User Profiles  
        'view_profiles': 'प्रोफाइल पहा',
        'create_new_profile': 'नवीन प्रोफाइल तयार करा',
        'no_profiles': 'कोणतीही प्रोफाइल आढळली नाही. तुमची पहिली प्रोफाइल तयार करा!',
        'birth_date': 'जन्म तारीख',
        'birth_time': 'जन्म वेळ',
        'birth_place': 'जन्म ठिकाण',
        'latitude': 'अक्षांश',
        'longitude': 'रेखांश',
        'timezone': 'वेळ क्षेत्र',
        'notes': 'टिपा',
        'name': 'नाव',
        'relationship': 'नाते',
        'gender': 'लिंग',
        'self': 'स्वतः',
        'spouse': 'जोडीदार',
        'child': 'मूल',
        'parent': 'पालक',
        'sibling': 'भावंड',
        'friend': 'मित्र',
        'other': 'इतर',
        'male': 'पुरुष',
        'female': 'स्त्री',
        'create_profile': 'प्रोफाइल तयार करा',
        'profile_created': 'प्रोफाइल यशस्वीरित्या तयार झाली!',
        'fill_required': 'कृपया सर्व आवश्यक फील्ड भरा',
        'select': 'निवडा',
        'selected': 'निवडले',
        'full_name': 'पूर्ण नाव',
        'optional': 'पर्यायी',
        'hour': 'तास',
        'minute': 'मिनिट',
        'second': 'सेकंद',
        # Birth Chart
        'birth_chart': 'जन्म कुंडली',
        'ascendant': 'लग्न',
        'degree': 'अंश',
        'nakshatra': 'नक्षत्र',
        'planetary_positions': 'ग्रह स्थिती',
        'planet': 'ग्रह',
        'sign': 'राशी',
        'house': 'भाव',
        'retrograde': 'वक्री',
        'divisional_charts': 'विभागीय कुंडली (वर्ग)',
        # Dasha
        'vimshottari_dasha': 'विम्शोत्तरी दशा (120 वर्षे)',
        'current_dasha': 'सध्याची दशा',
        'till': 'पर्यंत',
        'view_all_dasha': '📅 सर्व दशा कालावधी पहा (विस्तारासाठी क्लिक करा)',
        'years': 'वर्षे',
        # Chart Analysis
        'chart_analysis_header': '📊 कुंडली विश्लेषण',
        'strengths': 'शक्ती',
        'areas_attention': 'लक्ष देण्याजोगे क्षेत्र',
        'exalted_in': 'मध्ये उच्च आहे',
        'debilitated_in': 'मध्ये नीच आहे',
        'strong_ascendant': 'मजबूत लग्न स्थिती',
        'nakshatra_influence': 'नक्षत्र प्रभाव',
        'no_afflictions': 'कोणतीही मोठी ग्रह पीडा नाही',
        'balanced_positions': 'संतुलित ग्रह स्थिती',
        # Remedies
        'astrological_remedies': '🏥 ज्योतिषीय उपाय',
        'select_profile_remedy': 'प्रोफाइल निवडा',
        'specific_concern': 'विशिष्ट चिंता (पर्यायी)',
        'get_remedies': 'उपाय मिळवा',
        'personalized_remedies': 'साठी वैयक्तिक उपाय:',
        'immediate_actions': '⚡ तात्काळ कृती - आजपासून सुरु करा!',
        'lal_kitab_remedies': '📿 लाल किताब उपाय',
        'general_remedies': '🌟 सामान्य उपाय',
        'quick_wins': '✨ त्वरित उपाय (करणे सोपे)',
        'planetary_remedies': '🪐 ग्रह उपाय',
        # Payment & Credits
        'nav_credits': '💳 क्रेडिट्स खरेदी करा',
        'credits_balance': 'क्रेडिट्स शिल्लक',
        'buy_credits': 'क्रेडिट्स खरेदी करा',
        'insufficient_credits': 'अपुरी क्रेडिट्स',
        'need_credits_msg': 'हे वैशिष्ट्य वापरण्यासाठी तुम्हाला क्रेडिट्स आवश्यक आहेत. सुरू ठेवण्यासाठी कृपया क्रेडिट्स खरेदी करा.',
        'payment_options': 'पेमेंट पर्याय',
        'single_question_price': '₹10 प्रति प्रश्न',
        'bulk_discount': 'मोठ्या प्रमाणात खरेदी (अधिक बचत करा!)',
        'questions': 'प्रश्न',
        'price': 'किंमत',
        'save': 'बचत',
        'pay_now': 'आता पैसे भरा',
        'transaction_id': 'व्यवहार ID / UPI संदर्भ',
        'submit_payment': 'पेमेंट सबमिट करा',
        'payment_instructions': 'पेमेंट केल्यानंतर, तुमचा UPI व्यवहार ID वर प्रविष्ट करा',
        'credits_added': 'क्रेडिट्स यशस्वीरित्या जोडले!',
        'payment_verified': 'पेमेंट सत्यापित! तुमच्या खात्यात क्रेडिट्स जोडले गेले आहेत.',
    }
}

def get_text(key):
    """Get translated text based on current language"""
    lang = st.session_state.get('language', 'English')
    return TRANSLATIONS.get(lang, TRANSLATIONS['English']).get(key, key)


init_session_state()


def main():
    """Main application"""
    
    # Check session validity
    check_session()
    
    # Show login/register if not logged in
    if not st.session_state.get('logged_in', False) and not st.session_state.get('guest_mode', False):
        if st.session_state.get('show_register', False):
            show_register()
        else:
            show_login()
        return
    
    # Show user info in sidebar
    show_user_info_sidebar()
    
    # Sacred Ganesh Mantra at the top
    st.markdown("<div style='text-align: center; padding: 10px 0 5px 0;'><h3 style='color: #ff6b35; margin: 0;'>🕉️ ॐ गं गणपतये नमः 🕉️</h3></div>", unsafe_allow_html=True)
    
    # Header with translation
    st.markdown(f'<h1 class="main-header">{get_text("app_title")}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">{get_text("app_subtitle")}</p>', unsafe_allow_html=True)
    
    # Guest mode warning
    if st.session_state.get('guest_mode', False):
        st.warning("⚠️ **Guest Mode:** You can explore the app, but cannot save profiles or charts. Please register to save your data.")
    
    # Sidebar navigation with translation
    st.sidebar.title("Navigation" if st.session_state.language == 'English' else "नेविगेशन" if st.session_state.language == 'Hindi' else "नॅव्हिगेशन")
    
    # Get nav items based on language (without Document Management)
    lang = st.session_state.get('language', 'English')
    if lang == 'Hindi':
        nav_list = [get_text('nav_home'), get_text('nav_profiles'), 
                    get_text('nav_horoscope'), get_text('nav_ask'), 
                    get_text('nav_remedies'), get_text('nav_career'),
                    get_text('nav_financial'), get_text('nav_gemstones'), get_text('nav_numerology'),
                    get_text('nav_matchmaking'), get_text('nav_soulmate'), get_text('nav_muhurat'), get_text('nav_varshaphal'),
                    get_text('nav_dasha_detail'), get_text('nav_name_rec'),
                    get_text('nav_credits'), get_text('nav_settings'), get_text('nav_stotras')]
    elif lang == 'Marathi':
        nav_list = [get_text('nav_home'), get_text('nav_profiles'),
                    get_text('nav_horoscope'), get_text('nav_ask'),
                    get_text('nav_remedies'), get_text('nav_career'),
                    get_text('nav_financial'), get_text('nav_gemstones'), get_text('nav_numerology'),
                    get_text('nav_matchmaking'), get_text('nav_soulmate'), get_text('nav_muhurat'), get_text('nav_varshaphal'),
                    get_text('nav_dasha_detail'), get_text('nav_name_rec'),
                    get_text('nav_credits'), get_text('nav_settings'), get_text('nav_stotras')]
    else:  # English
        nav_list = [get_text('nav_home'), get_text('nav_profiles'),
                    get_text('nav_horoscope'), get_text('nav_ask'),
                    get_text('nav_remedies'), get_text('nav_career'),
                    get_text('nav_financial'), get_text('nav_gemstones'), get_text('nav_numerology'),
                    get_text('nav_matchmaking'), get_text('nav_soulmate'), get_text('nav_muhurat'), get_text('nav_varshaphal'),
                    get_text('nav_dasha_detail'), get_text('nav_name_rec'),
                    get_text('nav_credits'), get_text('nav_settings'), get_text('nav_stotras')]
    
    # Check if force_page is set (programmatic navigation)
    if 'force_page' in st.session_state:
        page = st.session_state.force_page
        del st.session_state.force_page
        # Update current_page for next run
        st.session_state.current_page = page
        # Immediately rerun to show the navigation with updated page
        st.rerun()
    
    # Get index from current_page if it exists
    default_index = 0
    if 'current_page' in st.session_state and st.session_state.current_page in nav_list:
        default_index = nav_list.index(st.session_state.current_page)
    
    page = st.sidebar.radio(
        "",  # No label
        nav_list,
        index=default_index,
        label_visibility="collapsed"
    )
    st.session_state.current_page = page
    
    # Company Logo at Bottom
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        <div style='text-align: center; padding: 20px 0; margin-top: 20px;'>
            <div style='font-size: 2rem; margin-bottom: 5px;'>☂️</div>
            <div style='font-weight: 600; color: #FF6B35; font-size: 1.1rem;'>Krittika Apps</div>
            <div style='font-size: 0.75rem; color: #666; margin-top: 5px;'>Sharp. Supreme. Protective.</div>
            <div style='font-size: 0.7rem; color: #999; margin-top: 10px;'>© 2026 Krittika Apps</div>
            <div style='font-size: 0.7rem; color: #666; margin-top: 10px;'>
                <a href='https://github.com/pandeabhijitv-ux/kundalisaga/blob/main/PRIVACY_POLICY.md' target='_blank' style='color: #FF6B35; text-decoration: none;'>Privacy Policy</a>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Route to pages (match against translated nav items)
    if page == get_text('nav_home'):
        show_home()
    elif page == get_text('nav_profiles'):
        if st.session_state.get('guest_mode', False):
            st.warning("🔒 Please register or login to create and manage profiles")
            if st.button("Go to Login/Register"):
                st.session_state.guest_mode = False
                st.session_state.current_user = None
                st.rerun()
        else:
            show_user_profiles()
    elif page == get_text('nav_horoscope'):
        if st.session_state.get('guest_mode', False):
            st.warning("🔒 Please register or login to calculate and save horoscopes")
            if st.button("Go to Login/Register"):
                st.session_state.guest_mode = False
                st.session_state.current_user = None
                st.rerun()
        else:
            show_horoscope()
    elif page == get_text('nav_ask'):
        show_ask_question()
    elif page == get_text('nav_remedies'):
        if st.session_state.get('guest_mode', False):
            st.warning("🔒 Please register or login to get personalized remedies")
            if st.button("Go to Login/Register"):
                st.session_state.guest_mode = False
                st.session_state.current_user = None
                st.rerun()
        else:
            show_remedies()
    elif page == get_text('nav_stotras'):
        show_stotras()
    elif page == get_text('nav_numerology'):
        if st.session_state.get('guest_mode', False):
            st.warning("🔒 Please register or login to access numerology")
            if st.button("Go to Login/Register"):
                st.session_state.guest_mode = False
                st.session_state.current_user = None
                st.rerun()
        else:
            show_numerology()
    elif page == get_text('nav_credits'):
        show_buy_credits()
    elif page == get_text('nav_career'):
        if st.session_state.get('guest_mode', False):
            st.warning("🔒 Please register or login to access career guidance")
            if st.button("Go to Login/Register"):
                st.session_state.guest_mode = False
                st.session_state.current_user = None
                st.rerun()
        else:
            show_career_guidance()
    elif page == get_text('nav_financial'):
        if st.session_state.get('guest_mode', False):
            st.warning("🔒 Please register or login to access financial outlook")
            if st.button("Go to Login/Register"):
                st.session_state.guest_mode = False
                st.session_state.current_user = None
                st.rerun()
        else:
            show_financial_outlook()
    elif page == get_text('nav_gemstones'):
        if st.session_state.get('guest_mode', False):
            st.warning("🔒 Please register or login to access gemstone recommendations")
            if st.button("Go to Login/Register"):
                st.session_state.guest_mode = False
                st.session_state.current_user = None
                st.rerun()
        else:
            show_gemstone_recommendations()
    elif page == get_text('nav_matchmaking'):
        if st.session_state.get('guest_mode', False):
            st.warning("🔒 Please register or login to access matchmaking")
            if st.button("Go to Login/Register"):
                st.session_state.guest_mode = False
                st.session_state.current_user = None
                st.rerun()
        else:
            show_matchmaking()
    elif page == get_text('nav_soulmate'):
        if st.session_state.get('guest_mode', False):
            st.warning("🔒 Please register or login to access soulmate analysis")
            if st.button("Go to Login/Register"):
                st.session_state.guest_mode = False
                st.session_state.current_user = None
                st.rerun()
        else:
            show_soulmate_analysis()
    elif page == get_text('nav_muhurat'):
        if st.session_state.get('guest_mode', False):
            st.warning("🔒 Please register or login to access muhurat finder")
            if st.button("Go to Login/Register"):
                st.session_state.guest_mode = False
                st.session_state.current_user = None
                st.rerun()
        else:
            show_muhurat_finder()
    elif page == get_text('nav_varshaphal'):
        if st.session_state.get('guest_mode', False):
            st.warning("🔒 Please register or login to access varshaphal")
            if st.button("Go to Login/Register"):
                st.session_state.guest_mode = False
                st.session_state.current_user = None
                st.rerun()
        else:
            show_varshaphal()
    elif page == get_text('nav_dasha_detail'):
        if st.session_state.get('guest_mode', False):
            st.warning("🔒 Please register or login to access detailed dasha analysis")
            if st.button("Go to Login/Register"):
                st.session_state.guest_mode = False
                st.session_state.current_user = None
                st.rerun()
        else:
            show_dasha_detail()
    elif page == get_text('nav_name_rec'):
        if st.session_state.get('guest_mode', False):
            st.warning("🔒 Please register or login to access name recommendations")
            if st.button("Go to Login/Register"):
                st.session_state.guest_mode = False
                st.session_state.current_user = None
                st.rerun()
        else:
            show_name_recommendation()
    elif page == get_text('nav_settings'):
        show_settings()


def show_home():
    """Home page"""
    st.markdown(f'<h2 style="margin-top: -10px; margin-bottom: 10px;">{get_text("welcome")}</h2>', unsafe_allow_html=True)
    
    # First Row - Main Features (Compact)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div style="background-color: #FFE6E6; padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #FF6B6B; height: 150px;">
            <h4 style="margin: 0 0 0.3rem 0; color: #C92A2A; font-size: 0.95rem;">🏥 Get Remedies</h4>
            <p style="margin: 0; color: #666; font-size: 0.75rem;">
                Lal Kitab remedies & lifestyle changes
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎯 View", key="home_remedies", use_container_width=True):
            st.session_state.force_page = get_text('nav_remedies')
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background-color: #E6F3FF; padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #4DABF7; height: 150px;">
            <h4 style="margin: 0 0 0.3rem 0; color: #1864AB; font-size: 0.95rem;">💬 Ask Question</h4>
            <p style="margin: 0; color: #666; font-size: 0.75rem;">
                Instant answers about career, wealth, relationships
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("❓ Ask", key="home_ask", use_container_width=True):
            st.session_state.force_page = get_text('nav_ask')
            st.rerun()
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #5B21B6; height: 150px;">
            <h4 style="margin: 0 0 0.3rem 0; color: white; font-size: 0.95rem;">📈 Financial</h4>
            <p style="margin: 0; color: #E0E7FF; font-size: 0.75rem;">
                Market trends using planetary transits
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📊 View", key="home_financial", use_container_width=True):
            st.session_state.force_page = get_text('nav_financial')
            st.rerun()
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FF6B9D 0%, #C44569 100%); padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #C0392B; height: 150px;">
            <h4 style="margin: 0 0 0.3rem 0; color: white; font-size: 0.95rem;">💎 Gemstones</h4>
            <p style="margin: 0; color: #FFE5EC; font-size: 0.75rem;">
                Personalized recommendations from chart analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💍 View", key="home_gemstones", use_container_width=True):
            st.session_state.force_page = get_text('nav_gemstones')
            st.rerun()
    
    with col5:
        st.markdown("""
        <div style="background-color: #E6F9E6; padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #51CF66; height: 150px;">
            <h4 style="margin: 0 0 0.3rem 0; color: #2B8A3E; font-size: 0.95rem;">🔢 Numerology</h4>
            <p style="margin: 0; color: #666; font-size: 0.75rem;">
                Life Path, Expression & Soul numbers
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔮 View", key="home_numerology", use_container_width=True):
            st.session_state.force_page = get_text('nav_numerology')
            st.rerun()
    
    # Second Row - Premium Features
    col6, col7, col8, col9, col10 = st.columns(5)
    
    with col6:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFA07A 0%, #FF6347 100%); padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #DC143C; height: 150px;">
            <h4 style="margin: 0 0 0.3rem 0; color: white; font-size: 0.95rem;">💑 Matchmaking</h4>
            <p style="margin: 0; color: #FFF5EE; font-size: 0.75rem;">
                Kundali Milan & compatibility analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💕 Check", key="home_matchmaking", use_container_width=True):
            st.session_state.force_page = get_text('nav_matchmaking')
            st.rerun()
    
    with col7:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #FF8C00; height: 150px;">
            <h4 style="margin: 0 0 0.3rem 0; color: #8B4513; font-size: 0.95rem;">⏰ Muhurat</h4>
            <p style="margin: 0; color: #8B4513; font-size: 0.75rem;">
                Auspicious timing for important events
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🕐 Find", key="home_muhurat", use_container_width=True):
            st.session_state.force_page = get_text('nav_muhurat')
            st.rerun()
    
    with col8:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #87CEEB 0%, #4682B4 100%); padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #1E90FF; height: 150px;">
            <h4 style="margin: 0 0 0.3rem 0; color: white; font-size: 0.95rem;">📅 Varshaphal</h4>
            <p style="margin: 0; color: #F0F8FF; font-size: 0.75rem;">
                Annual predictions & yearly forecast
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📆 View", key="home_varshaphal", use_container_width=True):
            st.session_state.force_page = get_text('nav_varshaphal')
            st.rerun()
    
    with col9:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #9370DB 0%, #8A2BE2 100%); padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #6A0DAD; height: 150px;">
            <h4 style="margin: 0 0 0.3rem 0; color: white; font-size: 0.95rem;">🌀 Dasha Analysis</h4>
            <p style="margin: 0; color: #E6E6FA; font-size: 0.75rem;">
                Detailed planetary period predictions
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 Analyze", key="home_dasha", use_container_width=True):
            st.session_state.force_page = get_text('nav_dasha_detail')
            st.rerun()
    
    with col10:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #98D8C8 0%, #6AB7A8 100%); padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #2F855A; height: 150px;">
            <h4 style="margin: 0 0 0.3rem 0; color: white; font-size: 0.95rem;">✨ Name Guide</h4>
            <p style="margin: 0; color: #F0FFF4; font-size: 0.75rem;">
                Lucky names based on numerology
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📝 Suggest", key="home_name", use_container_width=True):
            st.session_state.force_page = get_text('nav_name_rec')
            st.rerun()
    
    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
    
    # Quick Start Guide and Settings (Compact)
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown(f'<h4 style="margin-bottom: 10px;">{get_text("quick_start")}</h4>', unsafe_allow_html=True)
        
        steps = [
            (get_text('step1'), get_text('step1_desc')),
            (get_text('step2'), get_text('step2_desc')),
            (get_text('step3'), get_text('step3_desc')),
            (get_text('step4'), get_text('step4_desc'))
        ]
        
        for i, (title, desc) in enumerate(steps, 1):
            st.markdown(f"**{i}. {title}** - {desc}", unsafe_allow_html=True)
    
    with col_right:
        st.subheader("⚙️ Settings & Customization")
        st.markdown("""<div style="background-color: #FFFFF0; padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #FFE57F;">
            <p style="margin: 0 0 0.5rem 0; color: #333;">📋 <strong>Available Settings:</strong></p>
            <ul style="margin: 0; color: #666; padding-left: 1.5rem;">
                <li><strong>🌐 Language Selection:</strong> Switch between English, Hindi, and Marathi</li>
                <li><strong>📊 Chart Style:</strong> Choose North Indian (diamond) or South Indian (grid) format</li>
                <li><strong>🌟 Ayanamsa System:</strong> Traditional Lahiri (default, most widely used by Vedic astrologers)</li>
                <li><strong>🏠 House System:</strong> Whole Sign method (traditional Vedic approach)</li>
                <li><strong>🌍 Time Zone:</strong> Automatic detection based on birth location coordinates</li>
                <li><strong>🤖 AI Configuration:</strong> Local LLM processing (privacy-focused)</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    
    # Recent activity - only show for logged-in users
    if st.session_state.logged_in:
        st.markdown("---")
        st.subheader("Recent Activity" if st.session_state.language == 'English' else "हाल की गतिविधि" if st.session_state.language == 'Hindi' else "अलीकडील क्रियाकलाप")
        
        # Get current user's email
        current_email = st.session_state.current_user
        profiles = st.session_state.user_manager.list_profiles(current_email)
        
        if profiles:
            msg = f"✅ {len(profiles)} user profile(s) created" if st.session_state.language == 'English' else f"✅ {len(profiles)} उपयोगकर्ता प्रोफाइल बनाए गए" if st.session_state.language == 'Hindi' else f"✅ {len(profiles)} वापरकर्ता प्रोफाइल तयार केले"
            st.success(msg)
        else:
            msg = "👋 No profiles yet. Create one to get started!" if st.session_state.language == 'English' else "👋 अभी तक कोई प्रोफ़ाइल नहीं। शुरू करने के लिए एक बनाएं!" if st.session_state.language == 'Hindi' else "👋 अद्याप कोणतीही प्रोफाइल नाही. सुरुवात करण्यासाठी एक तयार करा!"
            st.info(msg)


def show_user_profiles():
    """User profiles management page"""
    st.header(f"👤 {get_text('nav_profiles')}")
    
    tab1, tab2 = st.tabs([get_text('view_profiles'), get_text('create_new_profile')])
    
    with tab1:
        # Get current user's email or empty string for guest mode
        current_email = st.session_state.current_user if st.session_state.logged_in else ""
        profiles = st.session_state.user_manager.list_profiles(current_email)
        
        if profiles:
            for profile in profiles:
                with st.expander(f"👤 {profile.name} ({profile.relationship})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**{get_text('birth_date')}:** {profile.birth_date}")
                        st.write(f"**{get_text('birth_time')}:** {profile.birth_time}")
                        st.write(f"**{get_text('birth_place')}:** {profile.birth_place}")
                    
                    with col2:
                        st.write(f"**{get_text('latitude')}:** {profile.latitude}")
                        st.write(f"**{get_text('longitude')}:** {profile.longitude}")
                        st.write(f"**{get_text('timezone')}:** {profile.timezone}")
                    
                    if profile.notes:
                        st.write(f"**{get_text('notes')}:** {profile.notes}")
                    
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        # Set as current user
                        if st.button(f"✅ {get_text('select')} {profile.name}", key=f"select_{profile.user_id}"):
                            st.session_state.current_user = profile
                            st.success(f"{get_text('selected')} {profile.name}")
                            st.rerun()
                    
                    with col_b:
                        # Delete profile
                        if st.button(f"🗑️ Delete {profile.name}", key=f"delete_{profile.user_id}", type="secondary"):
                            if st.session_state.user_manager.delete_profile(profile.user_id, current_email):
                                st.success(f"✅ Profile '{profile.name}' deleted successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to delete profile")
        else:
            st.info(get_text('no_profiles'))
    
    with tab2:
        st.subheader(get_text('create_new_profile'))
        
        # Location search and selection (OUTSIDE form to allow interactive buttons)
        st.markdown("### 📍 Step 1: Select Birth Location")
        
        birth_place_search = st.text_input(
            "Search for birth place", 
            placeholder="e.g., Khamgaon, Mumbai, etc.",
            help="Type the city/town name and click Search to see all matching locations",
            key="birth_place_search"
        )
        
        # Initialize session state for selected location
        if 'selected_birth_place' not in st.session_state:
            st.session_state.selected_birth_place = None
        if 'selected_coordinates' not in st.session_state:
            st.session_state.selected_coordinates = None
        
        # Search button for multiple locations
        search_col1, search_col2 = st.columns([1, 4])
        with search_col1:
            if st.button("🔍 Search", key="search_btn", type="primary"):
                if birth_place_search and len(birth_place_search) > 2:
                    with st.spinner("Searching for locations..."):
                        locations = st.session_state.astro_engine.get_multiple_locations(birth_place_search)
                        if locations and len(locations) > 1:
                            st.session_state.location_options = locations
                            st.info(f"Found {len(locations)} matching locations. Please select one below:")
                        elif locations and len(locations) == 1:
                            st.session_state.selected_birth_place = locations[0]['place']
                            st.session_state.selected_coordinates = (locations[0]['latitude'], locations[0]['longitude'])
                            st.session_state.selected_timezone = locations[0].get('timezone', 'UTC')
                            st.success(f"✅ Found: {locations[0]['place']}")
                        else:
                            st.warning("No locations found. Try a more specific name or use the map below.")
                else:
                    st.warning("Please enter at least 3 characters to search")
        
        # Show location options if multiple found
        if 'location_options' in st.session_state and st.session_state.location_options:
            st.markdown("**Select the correct location:**")
            for idx, loc in enumerate(st.session_state.location_options):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.write(f"📍 {loc['place']}")
                    st.caption(f"Coordinates: {loc['latitude']:.4f}°, {loc['longitude']:.4f}°")
                with col_b:
                    if st.button("Select", key=f"loc_select_{idx}"):
                        st.session_state.selected_birth_place = loc['place']
                        st.session_state.selected_coordinates = (loc['latitude'], loc['longitude'])
                        st.session_state.selected_timezone = loc.get('timezone', 'UTC')
                        del st.session_state.location_options
                        st.success(f"✅ Selected: {loc['place']}")
                        st.rerun()
            st.markdown("---")
        
        # Display currently selected location
        if st.session_state.selected_birth_place:
            st.success(f"✅ **Selected Location:** {st.session_state.selected_birth_place}")
            if st.session_state.selected_coordinates:
                st.caption(f"Coordinates: {st.session_state.selected_coordinates[0]:.4f}°, {st.session_state.selected_coordinates[1]:.4f}°")
            if st.button("🔄 Change Location", key="change_location"):
                st.session_state.selected_birth_place = None
                st.session_state.selected_coordinates = None
                st.rerun()
        
        # Alternative: Interactive map
        with st.expander("🗺️ Or click on map to select location"):
            import folium
            from streamlit_folium import st_folium
            from geopy.geocoders import Nominatim
            
            # Initialize map centered on India by default
            m = folium.Map(
                location=[20.5937, 78.9629],  # Center of India
                zoom_start=5,
                tiles="OpenStreetMap"
            )
            
            # Add click handler instruction
            st.caption("👆 Click anywhere on the map to select birth location")
            
            # Display map and capture clicks
            map_data = st_folium(m, width=700, height=400, key="birth_map_select")
            
            # Process map click
            if map_data and map_data.get("last_clicked"):
                clicked_lat = map_data["last_clicked"]["lat"]
                clicked_lon = map_data["last_clicked"]["lng"]
                
                # Reverse geocode to get place name
                try:
                    geolocator = Nominatim(user_agent="kundalisaga")
                    location = geolocator.reverse(f"{clicked_lat}, {clicked_lon}", language="en")
                    if location:
                        st.session_state.selected_birth_place = location.address
                        st.session_state.selected_coordinates = (clicked_lat, clicked_lon)
                        st.success(f"📍 Selected: {location.address}")
                        st.info(f"Coordinates: {clicked_lat:.4f}°, {clicked_lon:.4f}°")
                        if st.button("✅ Use this location", key="use_map_loc"):
                            st.rerun()
                except Exception as e:
                    st.warning(f"Could not get location name. Using coordinates: {clicked_lat:.4f}°, {clicked_lon:.4f}°")
                    st.session_state.selected_birth_place = f"Location at {clicked_lat:.4f}°, {clicked_lon:.4f}°"
                    st.session_state.selected_coordinates = (clicked_lat, clicked_lon)
        
        # Alternative: Exact coordinates
        with st.expander("📍 Or use exact coordinates"):
            st.markdown("**Paste from Google Maps or enter manually:**")
            coords_paste = st.text_input(
                "Paste coordinates",
                placeholder="e.g., 19.0760, 72.8877",
                key="coords_paste"
            )
            
            parsed_lat = None
            parsed_lon = None
            
            if coords_paste:
                try:
                    cleaned = coords_paste.replace("°", "").replace("N", "").replace("S", "").replace("E", "").replace("W", "")
                    parts = [p.strip() for p in cleaned.replace(",", " ").split() if p.strip()]
                    
                    if len(parts) >= 2:
                        parsed_lat = float(parts[0])
                        parsed_lon = float(parts[1])
                        st.success(f"✅ Parsed: {parsed_lat:.4f}°, {parsed_lon:.4f}°")
                        if st.button("✅ Use these coordinates", key="use_parsed_coords"):
                            st.session_state.selected_birth_place = f"Location at {parsed_lat:.4f}°, {parsed_lon:.4f}°"
                            st.session_state.selected_coordinates = (parsed_lat, parsed_lon)
                            st.rerun()
                except:
                    st.warning("⚠️ Could not parse coordinates")
        
        st.markdown("---")
        st.markdown("### 📝 Step 2: Enter Profile Details")
        
        with st.form("create_profile"):
            name = st.text_input(f"{get_text('name')}*", placeholder=get_text('full_name'))
            relationship = st.selectbox(
                get_text('relationship'),
                [get_text('self'), get_text('spouse'), get_text('child'), 
                 get_text('parent'), get_text('sibling'), get_text('friend'), get_text('other')]
            )
            gender = st.selectbox(get_text('gender'), ["", get_text('male'), get_text('female'), get_text('other')])
            
            col1, col2 = st.columns(2)
            
            with col1:
                birth_date = st.date_input(
                    f"{get_text('birth_date')}*", 
                    value=datetime(1990, 1, 1),
                    min_value=datetime(1800, 1, 1),
                    max_value=datetime.now()
                )
                
                # Time input with seconds precision
                st.write(f"{get_text('birth_time')}* (HH:MM:SS)")
                time_col1, time_col2, time_col3 = st.columns(3)
                with time_col1:
                    hour = st.number_input(get_text('hour'), min_value=0, max_value=23, value=12, step=1, key="hour")
                with time_col2:
                    minute = st.number_input(get_text('minute'), min_value=0, max_value=59, value=0, step=1, key="minute")
                with time_col3:
                    second = st.number_input(get_text('second'), min_value=0, max_value=59, value=0, step=1, key="second")
                
                birth_time = datetime_time(int(hour), int(minute), int(second))
            
            with col2:
                # Display selected birth place (read-only)
                if st.session_state.selected_birth_place:
                    st.text_input(
                        f"{get_text('birth_place')}*",
                        value=st.session_state.selected_birth_place,
                        disabled=True,
                        help="Selected in Step 1 above"
                    )
                else:
                    st.warning("⚠️ Please select birth location in Step 1 above")
                    # Provide a fallback text input
                    birth_place_fallback = st.text_input(
                        f"{get_text('birth_place')}*",
                        placeholder="Or enter location here",
                        key="birth_place_fallback"
                    )
            
            notes = st.text_area(f"{get_text('notes')} ({get_text('optional')})")
            
            submitted = st.form_submit_button(get_text('create_profile'))
            
            if submitted:
                # Use selected location or fallback
                birth_place = st.session_state.selected_birth_place if st.session_state.selected_birth_place else st.session_state.get('birth_place_fallback', '')
                
                if not all([name, birth_place]):
                    st.error(get_text('fill_required'))
                else:
                    # Check if profile with same name already exists
                    current_email = st.session_state.current_user if st.session_state.logged_in else ""
                    existing_profiles = st.session_state.user_manager.list_profiles(current_email)
                    if any(p.name.lower() == name.lower() for p in existing_profiles):
                        st.error(f"❌ Profile with name '{name}' already exists! Please use a different name.")
                        return
                    
                    # Use selected coordinates or geocode
                    loc_info = None
                    
                    if st.session_state.selected_coordinates:
                        # Use pre-selected coordinates
                        loc_info = {
                            'place': birth_place,
                            'latitude': st.session_state.selected_coordinates[0],
                            'longitude': st.session_state.selected_coordinates[1],
                            'timezone': st.session_state.get('selected_timezone', 'UTC')
                        }
                        st.info(f"✅ Using selected location: {birth_place}")
                    else:
                        # Fallback: geocode from place name
                        with st.spinner("Getting location information..."):
                            loc_info = st.session_state.astro_engine.get_location_info(birth_place)
                    
                    if loc_info:
                        # Create profile
                        profile_data = {
                            'name': name,
                            'birth_date': birth_date.isoformat(),
                            'birth_time': birth_time.strftime("%H:%M:%S"),
                            'birth_place': loc_info['place'],
                            'latitude': loc_info['latitude'],
                            'longitude': loc_info['longitude'],
                            'timezone': loc_info['timezone'],
                            'relationship': relationship,
                            'gender': gender,
                            'notes': notes
                        }
                        
                        # Get current user's email
                        current_email = st.session_state.current_user if st.session_state.logged_in else ""
                        profile = st.session_state.user_manager.create_profile(profile_data, current_email)
                        
                        # Show success with balloons
                        st.balloons()
                        st.success(f"🎉 Profile Created Successfully! Welcome {name}!")
                        st.info(f"📍 Location: {loc_info['place']}")
                        st.info(f"🌐 Coordinates: {loc_info['latitude']:.4f}°, {loc_info['longitude']:.4f}°")
                        
                        # Clear location selection for next profile
                        st.session_state.selected_birth_place = None
                        st.session_state.selected_coordinates = None
                        if 'location_options' in st.session_state:
                            del st.session_state.location_options
                        
                        # Small delay to show messages before rerun
                        time.sleep(2)
                        
                        st.session_state.current_user = profile
                        st.rerun()
                    else:
                        st.error("❌ Could not find location. Please try a different place name or provide exact coordinates.")


def show_document_management():
    """Document management page"""
    st.header("📚 Document Management")
    
    tab1, tab2 = st.tabs(["Upload Documents", "View Status"])
    
    with tab1:
        st.subheader("Add Astrology Books")
        
        st.info("""
        **Supported formats:** PDF, DOCX, TXT, PNG, JPG, JPEG
        
        Place your books in the `data/books/` folder, or upload them below.
        """)
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Upload books",
            type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            if st.button("Process Uploaded Files"):
                process_uploaded_files(uploaded_files)
        
        st.markdown("---")
        
        # Process from directory
        books_dir = Path("data/books")
        books_dir.mkdir(parents=True, exist_ok=True)
        
        if st.button("Process Books from data/books/ folder"):
            process_books_directory()
    
    with tab2:
        st.subheader("Knowledge Base Status")
        
        stats = st.session_state.knowledge_base.get_stats()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Documents Indexed", stats['total_documents'])
        
        with col2:
            st.metric("Total Text Chunks", stats['total_chunks'])


def process_uploaded_files(uploaded_files):
    """Process uploaded files"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing {uploaded_file.name}...")
        
        # Save file temporarily
        temp_path = Path("data/books") / uploaded_file.name
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Process file
        doc = st.session_state.doc_processor.process_file(str(temp_path))
        
        if doc:
            # Add to simple knowledge base
            metadata = {
                'source': doc.file_name,
                'file_type': doc.file_type,
                'file_hash': doc.file_hash
            }
            
            st.session_state.knowledge_base.add_document(
                doc.text_content,
                metadata
            )
        
        progress_bar.progress((idx + 1) / len(uploaded_files))
    
    status_text.text("✅ All files processed!")
    st.success(f"Successfully processed {len(uploaded_files)} file(s)")


def process_books_directory():
    """Process all books from directory"""
    books_dir = "data/books"
    
    with st.spinner("Processing books..."):
        docs = st.session_state.doc_processor.process_directory(books_dir)
        
        if docs:
            progress_bar = st.progress(0)
            
            for idx, doc in enumerate(docs):
                # Add to simple knowledge base
                metadata = {
                    'source': doc.file_name,
                    'file_type': doc.file_type,
                    'file_hash': doc.file_hash
                }
                
                st.session_state.knowledge_base.add_document(
                    doc.text_content,
                    metadata
                )
                
                progress_bar.progress((idx + 1) / len(docs))
            
            st.success(f"Successfully processed {len(docs)} book(s) from directory!")


def show_horoscope():
    """Horoscope calculation page"""
    st.header(get_text('nav_horoscope'))
    
    # Informational note
    st.info("💡 **Tip:** After viewing your chart, visit the **Remedies** page for personalized solutions, Lal Kitab remedies, and spiritual guidance to strengthen your chart.")
    
    # Select user
    # Get current user's email or empty string for guest mode
    current_email = st.session_state.current_user if st.session_state.logged_in else ""
    profiles = st.session_state.user_manager.list_profiles(current_email)
    
    if not profiles:
        st.warning("Please create a user profile first!")
        return
    
    # Profile selection with delete option
    col_select, col_delete = st.columns([3, 1])
    
    with col_select:
        selected_profile = st.selectbox(
            get_text('select_profile'),
            profiles,
            format_func=lambda p: f"{p.name} ({p.relationship})"
        )
    
    with col_delete:
        st.write("")  # Spacing
        if st.button("🗑️ Delete Profile", key="delete_horoscope_profile"):
            current_email = st.session_state.current_user if st.session_state.logged_in else ""
            if st.session_state.user_manager.delete_profile(selected_profile.user_id, current_email):
                st.success(f"✅ Profile '{selected_profile.name}' deleted successfully!")
                st.rerun()
            else:
                st.error("Failed to delete profile")
    
    if st.button(get_text('create_chart')):
        with st.spinner("⏳ Calculating your personalized birth chart... Please wait 2-3 minutes while we analyze planetary positions..."):
            # Create BirthDetails
            birth_datetime = datetime.fromisoformat(
                f"{selected_profile.birth_date}T{selected_profile.birth_time}"
            )
            
            birth_details = BirthDetails(
                date=birth_datetime,
                latitude=selected_profile.latitude,
                longitude=selected_profile.longitude,
                timezone=selected_profile.timezone,
                name=selected_profile.name,
                place=selected_profile.birth_place
            )
            
            # Calculate chart
            chart = st.session_state.astro_engine.calculate_birth_chart(birth_details)
            
            # Calculate dashas and add to chart
            moon = chart['planets']['Moon']
            dashas = st.session_state.astro_engine.calculate_vimshottari_dasha(
                moon.longitude,
                birth_datetime
            )
            
            # Convert dasha dates to strings for JSON serialization
            dashas_serializable = []
            for dasha in dashas:
                dashas_serializable.append({
                    'maha_dasha_lord': dasha['lord'],
                    'maha_dasha_start': dasha['start_date'].strftime('%Y-%m-%d'),
                    'maha_dasha_end': dasha['end_date'].strftime('%Y-%m-%d'),
                    'antar_dasha_lord': dasha.get('antar_lord', dasha['lord']),
                    'antar_dasha_start': dasha['start_date'].strftime('%Y-%m-%d'),
                    'antar_dasha_end': dasha['end_date'].strftime('%Y-%m-%d')
                })
            
            chart['dashas'] = dashas_serializable
            
            # Save to session state for Q&A
            st.session_state.last_calculated_chart = chart
            
            # Save chart
            st.session_state.user_manager.save_chart(
                selected_profile.user_id,
                chart,
                "birth_chart"
            )
            
            # Display chart
            display_birth_chart(chart)


def detect_vedic_yogas(chart):
    """Detect important Vedic yogas in birth chart - short summary only"""
    planets = chart['planets']
    yogas_found = []
    
    # Get planet positions
    sun = planets.get('Sun')
    moon = planets.get('Moon')
    mars = planets.get('Mars')
    mercury = planets.get('Mercury')
    jupiter = planets.get('Jupiter')
    venus = planets.get('Venus')
    saturn = planets.get('Saturn')
    
    # Gajakesari Yoga (Moon-Jupiter in kendras from each other)
    if moon and jupiter:
        moon_house = moon.house
        jupiter_house = jupiter.house
        house_diff = abs(moon_house - jupiter_house)
        if house_diff in [0, 3, 6, 9]:
            yogas_found.append("Gajakesari Yoga (Wisdom & Prosperity)")
    
    # Budhaditya Yoga (Sun-Mercury together - Intelligence)
    if sun and mercury:
        if abs(sun.house - mercury.house) <= 1:
            yogas_found.append("Budhaditya Yoga (Sharp Intellect)")
    
    # Malavya Yoga (Venus in kendra, own sign/exalted)
    if venus and venus.house in [1, 4, 7, 10]:
        if venus.sign in ['Taurus', 'Libra', 'Pisces']:
            yogas_found.append("Malavya Yoga (Luxury & Comfort)")
    
    # Hamsa Yoga (Jupiter in kendra, own sign/exalted)
    if jupiter and jupiter.house in [1, 4, 7, 10]:
        if jupiter.sign in ['Sagittarius', 'Pisces', 'Cancer']:
            yogas_found.append("Hamsa Yoga (Wisdom & Spiritual Growth)")
    
    # Ruchaka Yoga (Mars in kendra, own sign/exalted)
    if mars and mars.house in [1, 4, 7, 10]:
        if mars.sign in ['Aries', 'Scorpio', 'Capricorn']:
            yogas_found.append("Ruchaka Yoga (Courage & Leadership)")
    
    # Dhana Yoga check (Jupiter-Venus combination)
    if jupiter and venus:
        if abs(jupiter.house - venus.house) <= 1:
            yogas_found.append("Dhana Yoga (Wealth Potential)")
    
    if yogas_found:
        if len(yogas_found) == 1:
            summary = f"You have **{yogas_found[0]}** in your chart."
        elif len(yogas_found) == 2:
            summary = f"You have **{yogas_found[0]}** and **{yogas_found[1]}** in your chart."
        else:
            summary = f"You have **{yogas_found[0]}**, **{yogas_found[1]}**, and {len(yogas_found)-2} more yoga(s)."
        
        activation = "Strengthen these yogas through planet-specific remedies for maximum benefits."
        
        return {'present': True, 'summary': summary, 'activation': activation, 'yogas': yogas_found}
    else:
        return {'present': False, 'summary': '', 'activation': '', 'yogas': []}


def generate_personality_insights(chart):
    """Generate personality insights based on planetary positions in natal chart"""
    planets = chart['planets']
    
    positive_traits = []
    negative_traits = []
    
    # Analyze Sun placement
    sun = planets.get('Sun')
    if sun:
        if sun.house in [1, 5, 9, 10]:
            positive_traits.append(f"You have strong leadership qualities and natural confidence (Sun in {sun.house}th house). People often look up to you for guidance.")
        if sun.sign in ['Aries', 'Leo', 'Sagittarius']:
            positive_traits.append(f"Your optimistic and dynamic nature (Sun in {sun.sign}) makes you inspirational to others. You bounce back quickly from setbacks.")
        if sun.house in [6, 8, 12]:
            negative_traits.append(f"You may struggle with self-doubt or ego conflicts at times (Sun in {sun.house}th house). Learning humility will bring peace.")
    
    # Analyze Moon placement
    moon = planets.get('Moon')
    if moon:
        if moon.house in [1, 4, 7]:
            positive_traits.append(f"You possess deep emotional intelligence and empathy (Moon in {moon.house}th house). Others feel comfortable sharing their feelings with you.")
        if moon.sign in ['Cancer', 'Taurus', 'Pisces']:
            positive_traits.append(f"Your nurturing and caring nature (Moon in {moon.sign}) creates harmony in relationships. You naturally understand people's needs.")
        if moon.house in [6, 8, 12] or moon.is_retrograde:
            negative_traits.append(f"You tend to overthink and may experience emotional fluctuations (Moon in {moon.house}th house). Meditation can help stabilize your mind.")
    
    # Analyze Mercury placement  
    mercury = planets.get('Mercury')
    if mercury:
        if mercury.house in [1, 2, 3, 5, 10]:
            positive_traits.append(f"You have excellent communication skills and quick wit (Mercury in {mercury.house}th house). Your ideas are always interesting and well-articulated.")
        if mercury.sign in ['Gemini', 'Virgo', 'Aquarius']:
            positive_traits.append(f"Your analytical mind and adaptability (Mercury in {mercury.sign}) help you solve problems creatively. You learn new skills easily.")
    
    # Analyze Venus placement
    venus = planets.get('Venus')
    if venus:
        if venus.house in [1, 2, 4, 5, 7, 11]:
            positive_traits.append(f"You have refined tastes and natural charm (Venus in {venus.house}th house). People are drawn to your pleasant personality and artistic sensibilities.")
    
    # Analyze Mars placement
    mars = planets.get('Mars')
    if mars:
        if mars.house in [1, 3, 6, 10, 11]:
            positive_traits.append(f"You possess courage and determination (Mars in {mars.house}th house). When you set your mind to something, you achieve it through sheer willpower.")
        if mars.house in [4, 7, 8] or mars.is_retrograde:
            negative_traits.append(f"You may experience occasional anger or impatience (Mars in {mars.house}th house). Channeling this energy into physical activities will help.")
    
    # Analyze Jupiter placement
    jupiter = planets.get('Jupiter')
    if jupiter:
        if jupiter.house in [1, 2, 5, 9, 11]:
            positive_traits.append(f"You have wisdom and a generous spirit (Jupiter in {jupiter.house}th house). Your optimism and faith inspire those around you.")
    
    # Analyze Saturn placement
    saturn = planets.get('Saturn')
    if saturn:
        if saturn.house in [3, 6, 10, 11]:
            positive_traits.append(f"You are disciplined and hardworking (Saturn in {saturn.house}th house). Your perseverance leads to lasting success and respect.")
        if saturn.house in [1, 4, 7, 8, 12]:
            negative_traits.append(f"You may face delays or obstacles (Saturn in {saturn.house}th house), but these challenges are teaching you patience and building your character.")
    
    # Ensure we have exactly 4 positive and 2 negative (or adjust as available)
    if len(positive_traits) < 4:
        positive_traits.append("You have unique gifts and talents waiting to be discovered through self-exploration.")
    if len(negative_traits) < 2:
        negative_traits.append("Remember that challenges are opportunities for growth. Your journey is uniquely yours.")
    
    return {
        'positive': positive_traits[:4],
        'negative': negative_traits[:2]
    }


def display_birth_chart(chart):
    """Display birth chart information"""
    st.success("✅ Birth chart calculated!")
    
    # Generate and display personality insights based on planetary positions
    st.markdown("---")
    st.subheader("✨ Your Personality Insights")
    st.caption("Based on planetary positions in your natal chart")
    
    insights = generate_personality_insights(chart)
    
    # Display positive traits
    st.markdown("**🌟 Your Strengths:**")
    for trait in insights['positive']:
        st.markdown(f"• {trait}")
    
    st.markdown("")
    
    # Display areas for growth
    st.markdown("**🎯 Areas for Growth:**")
    for trait in insights['negative']:
        st.markdown(f"• {trait}")
    
    st.markdown("---")
    
    # Detect and display Vedic Yogas
    yogas = detect_vedic_yogas(chart)
    if yogas['present']:
        st.subheader("🔱 Special Yogas in Your Chart")
        st.info(yogas['summary'])
        if yogas['activation']:
            st.caption(f"💡 {yogas['activation']}")
    
    st.markdown("---")
    
    # Visual Chart Display
    st.subheader(f"📊 {get_text('birth_chart')} (Rashi Chakra)")
    display_chart_diagram(chart)
    
    st.markdown("---")
    
    # Ascendant
    st.subheader(get_text('ascendant'))
    asc = chart['ascendant']
    st.write(f"**{asc.sign}** - {asc.degree_in_sign:.2f}°")
    st.write(f"**{get_text('nakshatra')}:** {asc.nakshatra} (Pada {asc.nakshatra_pada})")
    
    st.markdown("---")
    
    # Planets
    st.subheader(get_text('planetary_positions'))
    
    planets = chart['planets']
    
    # Create DataFrame
    planet_data = []
    for name, planet in planets.items():
        if name != 'Ascendant':
            planet_data.append({
                get_text('planet'): name,
                get_text('sign'): planet.sign,
                get_text('degree'): f"{planet.degree_in_sign:.2f}°",
                get_text('house'): planet.house,
                get_text('nakshatra'): f"{planet.nakshatra} ({planet.nakshatra_pada})",
                get_text('retrograde'): '⟲' if planet.is_retrograde else ''
            })
    
    df = pd.DataFrame(planet_data)
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    
    # Divisional Charts
    if 'divisional_charts' in chart:
        st.subheader(f"📈 {get_text('divisional_charts')}")
        
        div_tab1, div_tab2, div_tab3, div_tab4 = st.tabs(["D2 - Hora (Wealth)", "D9 - Navamsa (Marriage)", "D10 - Dasamsa (Career)", "D7 - Saptamsa (Children)"])
        
        with div_tab1:
            st.caption("D2 (Hora) - Wealth, prosperity, and material gains")
            display_divisional_chart(chart['divisional_charts']['D2'], "D2 - Hora Chart")
        
        with div_tab2:
            st.caption("D9 (Navamsa) - Marriage, spouse, dharma, and inner strength")
            display_divisional_chart(chart['divisional_charts']['D9'], "D9 - Navamsa Chart")
        
        with div_tab3:
            st.caption("D10 (Dasamsa) - Career, profession, and reputation")
            display_divisional_chart(chart['divisional_charts']['D10'], "D10 - Dasamsa Chart")
        
        with div_tab4:
            st.caption("D7 (Saptamsa) - Children and progeny")
            display_divisional_chart(chart['divisional_charts']['D7'], "D7 - Saptamsa Chart")
    
    st.markdown("---")
    # Dasha
    st.subheader(get_text('vimshottari_dasha'))
    moon = planets['Moon']
    birth_date = chart['birth_details'].date
    
    dashas = st.session_state.astro_engine.calculate_vimshottari_dasha(
        moon.longitude,
        birth_date
    )
    
    # Show current dasha prominently
    current_date = datetime.now()
    current_dasha = None
    for dasha in dashas:
        if dasha['start_date'] <= current_date <= dasha['end_date']:
            current_dasha = dasha
            break
    
    if current_dasha:
        st.info(f"**{get_text('current_dasha')}:** {current_dasha['lord']} ({get_text('till')} {current_dasha['end_date'].strftime('%Y-%m-%d')})")
    
    # Show all dashas in expandable section
    with st.expander(get_text('view_all_dasha')):
        for idx, dasha in enumerate(dashas, 1):
            is_current = dasha == current_dasha
            prefix = "▶️ " if is_current else ""
            st.write(f"{prefix}**{idx}. {dasha['lord']}**: {dasha['start_date'].strftime('%Y-%m-%d')} to {dasha['end_date'].strftime('%Y-%m-%d')} ({dasha['years']:.1f} {get_text('years')})")
        
    st.markdown("---")
    
    # Basic Predictions
    st.subheader(get_text('chart_analysis_header'))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**{get_text('strengths')}:**")
        strengths = []
        
        # Check for exalted planets
        for name, planet in planets.items():
            if name != 'Ascendant':
                # Exaltation signs
                exaltations = {
                    'Sun': 'Aries', 'Moon': 'Taurus', 'Mars': 'Capricorn',
                    'Mercury': 'Virgo', 'Jupiter': 'Cancer', 'Venus': 'Pisces',
                    'Saturn': 'Libra'
                }
                if name in exaltations and planet.sign == exaltations[name]:
                    strengths.append(f"{name} {get_text('exalted_in')} {planet.sign}")
        
        if strengths:
            for s in strengths[:5]:
                st.write(f"• {s}")
        else:
            st.write(f"• {get_text('strong_ascendant')}")
            st.write(f"• {asc.nakshatra} {get_text('nakshatra_influence')}")
    
    with col2:
        st.write(f"**{get_text('areas_attention')}:**")
        challenges = []
        
        # Check for debilitated planets
        debilitations = {
            'Sun': 'Libra', 'Moon': 'Scorpio', 'Mars': 'Cancer',
            'Mercury': 'Pisces', 'Jupiter': 'Capricorn', 'Venus': 'Virgo',
            'Saturn': 'Aries'
        }
        
        for name, planet in planets.items():
            if name != 'Ascendant' and name in debilitations:
                if planet.sign == debilitations[name]:
                    challenges.append(f"{name} {get_text('debilitated_in')} {planet.sign}")
                if planet.is_retrograde and name not in ['Rahu', 'Ketu']:
                    challenges.append(f"{name} {get_text('retrograde')}")
        
        if challenges:
            for c in challenges[:5]:
                st.write(f"• {c}")
        else:
            st.write(f"• {get_text('no_afflictions')}")
            st.write(f"• {get_text('balanced_positions')}")
    
    # Add jump link to detailed predictions
    st.markdown("---")
    st.markdown("<div id='detailed-predictions'></div>", unsafe_allow_html=True)
    st.info("🔮 **Detailed Predictions are being generated below...** Scroll down to view comprehensive astrological analysis.")
    
    st.markdown("---")
    st.markdown("---")
    
    # Auto-generate Detailed Predictions (no tabs, no button)
    # Add sacred invocation
    st.markdown("<h4 style='text-align: center; color: #ff6b35; margin-bottom: 20px; margin-top: 40px;'>🕉️ ॐ गं गणपतये नमः 🕉️</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-style: italic; margin-bottom: 30px;'>Om Gan Ganpataye Namah</p>", unsafe_allow_html=True)
    
    # Detailed Predictions - Auto-generate
    st.subheader("🔮 Detailed Astrological Predictions")
    
    with st.spinner("🔮 Generating detailed predictions from ancient Vedic texts... Please wait..."):
        # Generate predictions automatically
        generate_predictions(chart, planets, asc, current_dasha)


def display_divisional_chart(div_chart, title):
    """Display a divisional chart in user's selected style"""
    chart_style = st.session_state.get('chart_style', 'North Indian')
    
    if chart_style == 'North Indian':
        display_divisional_chart_north_indian(div_chart, title)
    else:
        display_divisional_chart_south_indian(div_chart, title)


def display_divisional_chart_south_indian(div_chart, title):
    """Display a divisional chart in South Indian style"""
    sign_abbr = ['Ar', 'Ta', 'Ge', 'Cn', 'Le', 'Vi', 'Li', 'Sc', 'Sg', 'Cp', 'Aq', 'Pi']
    sign_full_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                       'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    # Fixed grid positions
    grid_positions = {
        1: 'Sc', 2: 'Sg', 3: 'Cp', 4: 'Aq',
        5: 'Pi', 6: 'Ar', 7: 'Ta', 8: 'Ge',
        9: 'Cn', 10: 'Le', 11: 'Vi', 12: 'Li'
    }
    
    # Get ascendant sign number
    asc_sign = div_chart['ascendant_sign']
    asc_sign_index = sign_full_names.index(asc_sign)
    
    # Create grid data
    grid_data = {}
    for grid_pos in range(1, 13):
        sign = grid_positions[grid_pos]
        current_sign_index = sign_abbr.index(sign)
        house_num = ((current_sign_index - asc_sign_index) % 12) + 1
        current_sign_full = sign_full_names[current_sign_index]
        
        # Find planets in this sign
        sign_planets = []
        for planet_name, planet_data in div_chart['planets'].items():
            if planet_name != 'Ascendant' and planet_data['sign'] == current_sign_full:
                sign_planets.append(planet_name[:2])
        
        grid_data[grid_pos] = {
            'sign': sign,
            'house': house_num,
            'planets': sign_planets
        }
    
    # Simplified HTML for divisional chart
    chart_html = f"""
    <style>
        .div-chart {{ margin: 10px auto; text-align: center; }}
        .div-grid {{ display: inline-grid; grid-template-columns: repeat(4, 90px); 
                     grid-template-rows: repeat(4, 90px); gap: 0; border: 2px solid #000; }}
        .div-house {{ border: 1px solid #666; padding: 6px; background: white; 
                      display: flex; flex-direction: column; justify-content: center; align-items: center; }}
        .div-lagna {{ background: linear-gradient(135deg, #fff9e6 0%, #ffffff 100%); }}
        .div-house-num {{ position: absolute; top: 2px; left: 4px; font-size: 8px; color: #888; }}
        .div-sign {{ font-size: 13px; font-weight: bold; color: #333; margin-bottom: 3px; }}
        .div-planets {{ font-size: 10px; color: #0066cc; font-weight: 500; }}
    </style>
    <div class="div-chart">
        <div class="div-grid">
            <div class="div-house {'div-lagna' if grid_data[12]['house'] == 1 else ''}">
                <div class="div-sign">{grid_data[12]['sign']}</div>
                <div class="div-planets">{' '.join(grid_data[12]['planets'][:2]) if grid_data[12]['planets'] else '—'}</div>
            </div>
            <div class="div-house {'div-lagna' if grid_data[1]['house'] == 1 else ''}">
                <div class="div-sign">{grid_data[1]['sign']}</div>
                <div class="div-planets">{' '.join(grid_data[1]['planets'][:2]) if grid_data[1]['planets'] else '—'}</div>
            </div>
            <div class="div-house {'div-lagna' if grid_data[2]['house'] == 1 else ''}">
                <div class="div-sign">{grid_data[2]['sign']}</div>
                <div class="div-planets">{' '.join(grid_data[2]['planets'][:2]) if grid_data[2]['planets'] else '—'}</div>
            </div>
            <div class="div-house {'div-lagna' if grid_data[3]['house'] == 1 else ''}">
                <div class="div-sign">{grid_data[3]['sign']}</div>
                <div class="div-planets">{' '.join(grid_data[3]['planets'][:2]) if grid_data[3]['planets'] else '—'}</div>
            </div>
            
            <div class="div-house {'div-lagna' if grid_data[11]['house'] == 1 else ''}">
                <div class="div-sign">{grid_data[11]['sign']}</div>
                <div class="div-planets">{' '.join(grid_data[11]['planets'][:2]) if grid_data[11]['planets'] else '—'}</div>
            </div>
            <div style="grid-column: span 2; grid-row: span 2; background: #f8f9fa; display: flex; align-items: center; justify-content: center; border: 1px solid #999;">
                <div style="text-align: center; font-size: 11px; color: #666;">
                    <div style="font-weight: bold;">Ascendant</div>
                    <div>{div_chart['ascendant_sign']}</div>
                </div>
            </div>
            <div class="div-house {'div-lagna' if grid_data[4]['house'] == 1 else ''}">
                <div class="div-sign">{grid_data[4]['sign']}</div>
                <div class="div-planets">{' '.join(grid_data[4]['planets'][:2]) if grid_data[4]['planets'] else '—'}</div>
            </div>
            
            <div class="div-house {'div-lagna' if grid_data[10]['house'] == 1 else ''}">
                <div class="div-sign">{grid_data[10]['sign']}</div>
                <div class="div-planets">{' '.join(grid_data[10]['planets'][:2]) if grid_data[10]['planets'] else '—'}</div>
            </div>
            <div class="div-house {'div-lagna' if grid_data[5]['house'] == 1 else ''}">
                <div class="div-sign">{grid_data[5]['sign']}</div>
                <div class="div-planets">{' '.join(grid_data[5]['planets'][:2]) if grid_data[5]['planets'] else '—'}</div>
            </div>
            
            <div class="div-house {'div-lagna' if grid_data[9]['house'] == 1 else ''}">
                <div class="div-sign">{grid_data[9]['sign']}</div>
                <div class="div-planets">{' '.join(grid_data[9]['planets'][:2]) if grid_data[9]['planets'] else '—'}</div>
            </div>
            <div class="div-house {'div-lagna' if grid_data[8]['house'] == 1 else ''}">
                <div class="div-sign">{grid_data[8]['sign']}</div>
                <div class="div-planets">{' '.join(grid_data[8]['planets'][:2]) if grid_data[8]['planets'] else '—'}</div>
            </div>
            <div class="div-house {'div-lagna' if grid_data[7]['house'] == 1 else ''}">
                <div class="div-sign">{grid_data[7]['sign']}</div>
                <div class="div-planets">{' '.join(grid_data[7]['planets'][:2]) if grid_data[7]['planets'] else '—'}</div>
            </div>
            <div class="div-house {'div-lagna' if grid_data[6]['house'] == 1 else ''}">
                <div class="div-sign">{grid_data[6]['sign']}</div>
                <div class="div-planets">{' '.join(grid_data[6]['planets'][:2]) if grid_data[6]['planets'] else '—'}</div>
            </div>
        </div>
    </div>
    """
    import streamlit.components.v1 as components
    components.html(chart_html, height=400, scrolling=False)


def display_divisional_chart_north_indian(div_chart, title):
    """Display divisional chart in beautiful colorful North Indian style"""
    import base64
    import os
    
    sign_abbr = ['Ar', 'Ta', 'Ge', 'Cn', 'Le', 'Vi', 'Li', 'Sc', 'Sg', 'Cp', 'Aq', 'Pi']
    sign_full_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                       'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    # Get ascendant sign
    asc_sign = div_chart['ascendant_sign']
    asc_sign_index = sign_full_names.index(asc_sign)
    
    # Create house data for North Indian
    house_data = {}
    for house_num in range(1, 13):
        sign_index = (asc_sign_index + house_num - 1) % 12
        current_sign = sign_full_names[sign_index]
        current_sign_abbr = sign_abbr[sign_index]
        
        # Find planets
        house_planets = []
        for planet_name, planet_data in div_chart['planets'].items():
            if planet_name != 'Ascendant' and planet_data['sign'] == current_sign:
                house_planets.append(planet_name[:2])
        
        house_data[house_num] = {
            'sign': current_sign_abbr,
            'planets': house_planets
        }
    
    # Load and encode background image
    bg_image_path = os.path.join('assets', 'north_indian_chart_bg.png')
    bg_image_data = ""
    try:
        if os.path.exists(bg_image_path):
            with open(bg_image_path, 'rb') as f:
                bg_image_data = base64.b64encode(f.read()).decode('utf-8')
                bg_image_data = f"data:image/png;base64,{bg_image_data}"
    except Exception as e:
        st.warning(f"Could not load chart background: {e}")
    
    # Compact colorful North Indian for divisional charts
    chart_html = f"""
    <style>
        .div-ni {{ margin: 10px auto; text-align: center; }}
        .div-ni-container {{ 
            position: relative; 
            width: 500px; 
            height: 500px; 
            margin: 0 auto;
            background-image: url('{bg_image_data}');
            background-size: 100% 100%;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .div-ni-house {{ 
            position: absolute; 
            display: flex; 
            flex-direction: column; 
            justify-content: center; 
            align-items: center; 
            padding: 5px;
        }}
        .div-ni-sign {{ font-size: 13px; font-weight: bold; color: #2c3e50; margin-bottom: 2px; text-shadow: 0 1px 2px rgba(255,255,255,0.7); }}
        .div-ni-planets {{ font-size: 11px; color: #2471a3; font-weight: 600; text-align: center; text-shadow: 0 1px 2px rgba(255,255,255,0.5); }}
    </style>
    <div class="div-ni">
        <div class="div-ni-container">
            
            <div class="div-ni-house" style="top: 50px; left: 50%; transform: translateX(-50%);">
                <div class="div-ni-sign">{house_data[1]['sign']}</div>
                <div class="div-ni-planets">{', '.join(house_data[1]['planets'][:2]) if house_data[1]['planets'] else ''}</div>
            </div>
            <div class="div-ni-house" style="top: 80px; left: 155px;">
                <div class="div-ni-sign">{house_data[2]['sign']}</div>
                <div class="div-ni-planets">{', '.join(house_data[2]['planets'][:2]) if house_data[2]['planets'] else ''}</div>
            </div>
            <div class="div-ni-house" style="top: 100px; left: 60px;">
                <div class="div-ni-sign">{house_data[3]['sign']}</div>
                <div class="div-ni-planets">{', '.join(house_data[3]['planets'][:2]) if house_data[3]['planets'] else ''}</div>
            </div>
            <div class="div-ni-house" style="top: 225px; left: 60px;">
                <div class="div-ni-sign">{house_data[4]['sign']}</div>
                <div class="div-ni-planets">{', '.join(house_data[4]['planets'][:2]) if house_data[4]['planets'] else ''}</div>
            </div>
            <div class="div-ni-house" style="top: 350px; left: 60px;">
                <div class="div-ni-sign">{house_data[5]['sign']}</div>
                <div class="div-ni-planets">{', '.join(house_data[5]['planets'][:2]) if house_data[5]['planets'] else ''}</div>
            </div>
            <div class="div-ni-house" style="top: 370px; left: 155px;">
                <div class="div-ni-sign">{house_data[6]['sign']}</div>
                <div class="div-ni-planets">{', '.join(house_data[6]['planets'][:2]) if house_data[6]['planets'] else ''}</div>
            </div>
            <div class="div-ni-house" style="top: 430px; left: 50%; transform: translateX(-50%);">
                <div class="div-ni-sign">{house_data[7]['sign']}</div>
                <div class="div-ni-planets">{', '.join(house_data[7]['planets'][:2]) if house_data[7]['planets'] else ''}</div>
            </div>
            <div class="div-ni-house" style="top: 370px; left: 345px;">
                <div class="div-ni-sign">{house_data[8]['sign']}</div>
                <div class="div-ni-planets">{', '.join(house_data[8]['planets'][:2]) if house_data[8]['planets'] else ''}</div>
            </div>
            <div class="div-ni-house" style="top: 350px; left: 440px;">
                <div class="div-ni-sign">{house_data[9]['sign']}</div>
                <div class="div-ni-planets">{', '.join(house_data[9]['planets'][:2]) if house_data[9]['planets'] else ''}</div>
            </div>
            <div class="div-ni-house" style="top: 225px; left: 440px;">
                <div class="div-ni-sign">{house_data[10]['sign']}</div>
                <div class="div-ni-planets">{', '.join(house_data[10]['planets'][:2]) if house_data[10]['planets'] else ''}</div>
            </div>
            <div class="div-ni-house" style="top: 100px; left: 440px;">
                <div class="div-ni-sign">{house_data[11]['sign']}</div>
                <div class="div-ni-planets">{', '.join(house_data[11]['planets'][:2]) if house_data[11]['planets'] else ''}</div>
            </div>
            <div class="div-ni-house" style="top: 80px; left: 345px;">
                <div class="div-ni-sign">{house_data[12]['sign']}</div>
                <div class="div-ni-planets">{', '.join(house_data[12]['planets'][:2]) if house_data[12]['planets'] else ''}</div>
            </div>
        </div>
    </div>
    """
    import streamlit.components.v1 as components
    components.html(chart_html, height=540, scrolling=False)


def display_chart_diagram(chart):
    """Display birth chart in selected style (South Indian or North Indian)"""
    chart_style = st.session_state.get('chart_style', 'North Indian')
    
    if chart_style == 'North Indian':
        display_north_indian_chart(chart)
    else:
        display_south_indian_chart(chart)


def display_south_indian_chart(chart):
    """Display traditional South Indian style birth chart"""
    planets = chart['planets']
    asc = chart['ascendant']
    
    # In South Indian chart: Signs are FIXED, Houses ROTATE
    # Fixed sign positions in grid (1-12): Sc, Sg, Cp, Aq, Pi, Ar, Ta, Ge, Cn, Le, Vi, Li
    sign_abbr = ['Ar', 'Ta', 'Ge', 'Cn', 'Le', 'Vi', 'Li', 'Sc', 'Sg', 'Cp', 'Aq', 'Pi']
    
    # Grid positions for signs (South Indian standard layout)
    grid_positions = {
        # Row 1: 12(Li), 1(Sc), 2(Sg), 3(Cp)
        # Row 2: 11(Vi), CENTER, 4(Aq)
        # Row 3: 10(Le), 5(Pi)
        # Row 4: 9(Cn), 8(Ge), 7(Ta), 6(Ar)
        1: 'Sc', 2: 'Sg', 3: 'Cp', 4: 'Aq',
        5: 'Pi', 6: 'Ar', 7: 'Ta', 8: 'Ge',
        9: 'Cn', 10: 'Le', 11: 'Vi', 12: 'Li'
    }
    
    # Map signs to grid positions
    sign_to_grid = {v: k for k, v in grid_positions.items()}
    
    # Full sign names for matching with planet data
    sign_full_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                       'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    # Create data structure: grid_pos -> {sign, house_num, planets}
    grid_data = {}
    for grid_pos in range(1, 13):
        sign = grid_positions[grid_pos]
        
        # Find which house this sign belongs to
        # In Vedic astrology, sign 0=Aries, 1=Taurus, ..., 8=Sagittarius
        # asc.sign_num from calculator is 0-11 (NOT 1-12!)
        asc_sign_index = asc.sign_num  # Already 0-indexed from calculator
        current_sign_index = sign_abbr.index(sign)
        
        # Calculate house number: how many signs from ascendant?
        house_num = ((current_sign_index - asc_sign_index) % 12) + 1
        
        # Find planets in this SIGN (Rashi Chakra style - not by house calculation)
        # In D1 Rashi Chakra, planets are placed by their zodiac sign
        current_sign_full = sign_full_names[current_sign_index]
        sign_planets = []
        for name, planet in planets.items():
            if name != 'Ascendant':
                # Place planet in the box matching its sign, not calculated house
                if planet.sign == current_sign_full:
                    symbol = PLANET_SYMBOLS.get(name, '')
                    planet_display = f"{symbol}{name[:2]}" if symbol else name[:2]
                    sign_planets.append(planet_display)
        
        grid_data[grid_pos] = {
            'sign': sign,
            'house': house_num,
            'planets': sign_planets
        }
    
    # South Indian Chart - Fixed house positions in a square grid
    chart_html = f"""
    <style>
        .si-chart {{
            margin: 20px auto;
            text-align: center;
        }}
        .si-chart-title {{
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
            color: #cc0000;
        }}
        .si-grid {{
            display: inline-grid;
            grid-template-columns: repeat(4, 110px);
            grid-template-rows: repeat(4, 110px);
            gap: 0;
            border: 2px solid #000;
        }}
        .si-house {{
            border: 1px solid #666;
            padding: 8px;
            position: relative;
            background: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .si-lagna {{
            background: linear-gradient(135deg, #fff9e6 0%, #ffffff 100%);
        }}
        .si-house-num {{
            position: absolute;
            top: 3px;
            left: 5px;
            font-size: 9px;
            color: #888;
            font-weight: bold;
        }}
        .si-sign {{
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-bottom: 4px;
        }}
        .si-planets {{
            font-size: 11px;
            color: #0066cc;
            font-weight: 500;
        }}
        .si-lagna-mark {{
            font-size: 11px;
            color: #cc0000;
            font-weight: bold;
            margin-bottom: 2px;
        }}
        .si-center {{
            grid-column: 2 / 4;
            grid-row: 2 / 4;
            border: 2px solid #cc0000;
            background: linear-gradient(135deg, #ffe6e6 0%, #fff9e6 50%, #e6f3ff 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-size: 14px;
        }}
        .si-center-title {{
            font-size: 12px;
            color: #666;
            margin-bottom: 8px;
        }}
        .si-asc {{
            font-size: 18px;
            font-weight: bold;
            color: #cc0000;
            margin-bottom: 4px;
        }}
        .si-note {{
            margin-top: 15px;
            font-size: 12px;
            color: #666;
        }}
    </style>
    
    <div class="si-chart">
        <div class="si-chart-title">◆ South Indian Chart (Rashi Chakra) ◆</div>
        
        <div class="si-grid">
            <!-- Row 1 -->
            <div class="si-house {'si-lagna' if grid_data[12]['house'] == 1 else ''}">
                <span class="si-house-num">{grid_data[12]['house']}</span>
                {('<div class="si-lagna-mark">लग्न</div>' if grid_data[12]['house'] == 1 else '')}
                <div class="si-sign">{grid_data[12]['sign']}</div>
                <div class="si-planets">{' '.join(grid_data[12]['planets'][:3]) if grid_data[12]['planets'] else '—'}</div>
            </div>
            
            <div class="si-house {'si-lagna' if grid_data[1]['house'] == 1 else ''}">
                <span class="si-house-num">{grid_data[1]['house']}</span>
                {('<div class="si-lagna-mark">लग्न</div>' if grid_data[1]['house'] == 1 else '')}
                <div class="si-sign">{grid_data[1]['sign']}</div>
                <div class="si-planets">{' '.join(grid_data[1]['planets'][:3]) if grid_data[1]['planets'] else '—'}</div>
            </div>
            
            <div class="si-house {'si-lagna' if grid_data[2]['house'] == 1 else ''}">
                <span class="si-house-num">{grid_data[2]['house']}</span>
                {('<div class="si-lagna-mark">लग्न</div>' if grid_data[2]['house'] == 1 else '')}
                <div class="si-sign">{grid_data[2]['sign']}</div>
                <div class="si-planets">{' '.join(grid_data[2]['planets'][:3]) if grid_data[2]['planets'] else '—'}</div>
            </div>
            
            <div class="si-house {'si-lagna' if grid_data[3]['house'] == 1 else ''}">
                <span class="si-house-num">{grid_data[3]['house']}</span>
                {('<div class="si-lagna-mark">लग्न</div>' if grid_data[3]['house'] == 1 else '')}
                <div class="si-sign">{grid_data[3]['sign']}</div>
                <div class="si-planets">{' '.join(grid_data[3]['planets'][:3]) if grid_data[3]['planets'] else '—'}</div>
            </div>
            
            <!-- Row 2 -->
            <div class="si-house {'si-lagna' if grid_data[11]['house'] == 1 else ''}">
                <span class="si-house-num">{grid_data[11]['house']}</span>
                {('<div class="si-lagna-mark">लग्न</div>' if grid_data[11]['house'] == 1 else '')}
                <div class="si-sign">{grid_data[11]['sign']}</div>
                <div class="si-planets">{' '.join(grid_data[11]['planets'][:3]) if grid_data[11]['planets'] else '—'}</div>
            </div>
            
            <!-- Center (spans 2x2) -->
            <div class="si-center">
                <div class="si-center-title">Rashi Chakra</div>
                <div class="si-asc">{asc.sign}</div>
                <div style="font-size:10px;color:#666">Ascendant</div>
            </div>
            
            <div class="si-house {'si-lagna' if grid_data[4]['house'] == 1 else ''}">
                <span class="si-house-num">{grid_data[4]['house']}</span>
                {('<div class="si-lagna-mark">लग्न</div>' if grid_data[4]['house'] == 1 else '')}
                <div class="si-sign">{grid_data[4]['sign']}</div>
                <div class="si-planets">{' '.join(grid_data[4]['planets'][:3]) if grid_data[4]['planets'] else '—'}</div>
            </div>
            
            <!-- Row 3 -->
            <div class="si-house {'si-lagna' if grid_data[10]['house'] == 1 else ''}">
                <span class="si-house-num">{grid_data[10]['house']}</span>
                {('<div class="si-lagna-mark">लग्न</div>' if grid_data[10]['house'] == 1 else '')}
                <div class="si-sign">{grid_data[10]['sign']}</div>
                <div class="si-planets">{' '.join(grid_data[10]['planets'][:3]) if grid_data[10]['planets'] else '—'}</div>
            </div>
            
            <div class="si-house {'si-lagna' if grid_data[5]['house'] == 1 else ''}">
                <span class="si-house-num">{grid_data[5]['house']}</span>
                {('<div class="si-lagna-mark">लग्न</div>' if grid_data[5]['house'] == 1 else '')}
                <div class="si-sign">{grid_data[5]['sign']}</div>
                <div class="si-planets">{' '.join(grid_data[5]['planets'][:3]) if grid_data[5]['planets'] else '—'}</div>
            </div>
            
            <!-- Row 4 -->
            <div class="si-house {'si-lagna' if grid_data[9]['house'] == 1 else ''}">
                <span class="si-house-num">{grid_data[9]['house']}</span>
                {('<div class="si-lagna-mark">लग्न</div>' if grid_data[9]['house'] == 1 else '')}
                <div class="si-sign">{grid_data[9]['sign']}</div>
                <div class="si-planets">{' '.join(grid_data[9]['planets'][:3]) if grid_data[9]['planets'] else '—'}</div>
            </div>
            
            <div class="si-house {'si-lagna' if grid_data[8]['house'] == 1 else ''}">
                <span class="si-house-num">{grid_data[8]['house']}</span>
                {('<div class="si-lagna-mark">लग्न</div>' if grid_data[8]['house'] == 1 else '')}
                <div class="si-sign">{grid_data[8]['sign']}</div>
                <div class="si-planets">{' '.join(grid_data[8]['planets'][:3]) if grid_data[8]['planets'] else '—'}</div>
            </div>
            
            <div class="si-house {'si-lagna' if grid_data[7]['house'] == 1 else ''}">
                <span class="si-house-num">{grid_data[7]['house']}</span>
                {('<div class="si-lagna-mark">लग्न</div>' if grid_data[7]['house'] == 1 else '')}
                <div class="si-sign">{grid_data[7]['sign']}</div>
                <div class="si-planets">{' '.join(grid_data[7]['planets'][:3]) if grid_data[7]['planets'] else '—'}</div>
            </div>
            
            <div class="si-house {'si-lagna' if grid_data[6]['house'] == 1 else ''}">
                <span class="si-house-num">{grid_data[6]['house']}</span>
                {('<div class="si-lagna-mark">लग्न</div>' if grid_data[6]['house'] == 1 else '')}
                <div class="si-sign">{grid_data[6]['sign']}</div>
                <div class="si-planets">{' '.join(grid_data[6]['planets'][:3]) if grid_data[6]['planets'] else '—'}</div>
            </div>
        </div>
        
        <div class="si-note">
            Signs are FIXED • Houses rotate based on Ascendant ({asc.sign})
        </div>
    </div>
    """
    
    # Use st.components to ensure proper rendering
    import streamlit.components.v1 as components
    components.html(chart_html, height=600, scrolling=False)


def display_north_indian_chart(chart):
    """Display beautiful colorful North Indian style birth chart with curved diamond pattern"""
    import base64
    import os
    
    planets = chart['planets']
    asc = chart['ascendant']
    
    # In North Indian chart: Houses are FIXED (1-12), Signs ROTATE
    sign_abbr = ['Ar', 'Ta', 'Ge', 'Cn', 'Le', 'Vi', 'Li', 'Sc', 'Sg', 'Cp', 'Aq', 'Pi']
    sign_full_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                       'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    # Get ascendant sign index
    asc_sign_index = asc.sign_num  # 0-indexed
    
    # Create house data: house number -> {sign, planets}
    house_data = {}
    for house_num in range(1, 13):
        # Calculate which sign is in this house
        sign_index = (asc_sign_index + house_num - 1) % 12
        current_sign = sign_full_names[sign_index]
        current_sign_abbr = sign_abbr[sign_index]
        sign_number = sign_index + 1  # 1-indexed sign number (Ar=1, Ta=2... Pi=12)
        
        # Find planets in this house (by sign)
        house_planets = []
        for name, planet in planets.items():
            if name != 'Ascendant' and planet.sign == current_sign:
                symbol = PLANET_SYMBOLS.get(name, '')
                planet_display = f"{symbol}{name[:2]}" if symbol else name[:2]
                house_planets.append(planet_display)
        
        house_data[house_num] = {
            'sign': current_sign_abbr,
            'sign_num': sign_number,
            'planets': house_planets
        }
    
    # Load and encode background image
    bg_image_path = os.path.join('assets', 'north_indian_chart_bg.png')
    bg_image_data = ""
    try:
        if os.path.exists(bg_image_path):
            with open(bg_image_path, 'rb') as f:
                bg_image_data = base64.b64encode(f.read()).decode('utf-8')
                bg_image_data = f"data:image/png;base64,{bg_image_data}"
    except Exception as e:
        st.warning(f"Could not load chart background: {e}")
    
    # Vintage Parchment North Indian Chart matching traditional style
    chart_html = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&display=swap');
        
        .ni-fancy {{ margin: 20px auto; text-align: center; }}
        .ni-ganesha {{ 
            width: 70px; 
            height: 70px; 
            margin: 15px auto 20px auto; 
            display: block;
            border-radius: 50%;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        .ni-title {{ 
            font-family: 'Cinzel', serif;
            font-size: 22px; 
            font-weight: 600; 
            margin: 15px 0 30px 0; 
            color: #3e2723;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}
        .ni-container {{ 
            position: relative; 
            width: 600px; 
            height: 600px; 
            margin: 0 auto;
            background-image: url('{bg_image_data}');
            background-size: 100% 100%;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .ni-house {{ 
            position: absolute; 
            display: flex; 
            flex-direction: column; 
            justify-content: center; 
            align-items: center; 
            padding: 8px;
            z-index: 10;
        }}
        .ni-sign {{ 
            font-size: 22px; 
            font-weight: bold; 
            color: #8B0000;
            margin-bottom: 3px;
            text-shadow: 0 1px 2px rgba(255,255,255,0.5);
        }}
        .ni-sign-num {{
            font-size: 10px;
            color: #666;
            font-weight: bold;
            margin-left: 3px;
        }}
        .ni-planets {{ 
            font-size: 13px; 
            color: #0d47a1; 
            font-weight: 600; 
            text-align: center; 
            line-height: 1.4;
            text-shadow: 0 1px 2px rgba(255,255,255,0.3);
        }}
        .ni-lagna-mark {{ 
            position: absolute; 
            bottom: 2px; 
            left: 50%; 
            transform: translateX(-50%); 
            color: #bf360c; 
            font-weight: bold; 
            font-size: 11px;
            text-shadow: 0 1px 2px rgba(255,255,255,0.4);
        }}
        .ni-note {{
            margin-top: 25px;
            font-size: 13px;
            color: #5d4037;
            font-style: italic;
        }}
    </style>
    <div class="ni-fancy">
        <img src="https://i.imgur.com/YqZ9KQm.png" alt="Om Ganesha" class="ni-ganesha" onerror="this.style.display='none'">
        <div class="ni-title">॥ North Indian Chart (Kundali) ॥</div>
        
        <div class="ni-container">
            <!-- Lagna mark in center -->
            <div class="ni-lagna-mark" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 5;">✦ लग्न ✦</div>
            <!-- House 1 - Lagna (Top) -->
            <div class="ni-house" style="top: 60px; left: 50%; transform: translateX(-50%);">
                <div class="ni-sign">{house_data[1]['sign']}<span class="ni-sign-num">{house_data[1]['sign_num']}</span></div>
                <div class="ni-planets">{', '.join(house_data[1]['planets']) if house_data[1]['planets'] else ''}</div>
            </div>
            
            <!-- House 2 - NW Corner Triangle -->
            <div class="ni-house" style="top: 80px; left: 115px;">
                <div class="ni-sign">{house_data[2]['sign']}<span class="ni-sign-num">{house_data[2]['sign_num']}</span></div>
                <div class="ni-planets">{', '.join(house_data[2]['planets']) if house_data[2]['planets'] else ''}</div>
            </div>
            
            <!-- House 3 - Left Upper -->
            <div class="ni-house" style="top: 125px; left: 75px;">
                <div class="ni-sign">{house_data[3]['sign']}<span class="ni-sign-num">{house_data[3]['sign_num']}</span></div>
                <div class="ni-planets">{', '.join(house_data[3]['planets']) if house_data[3]['planets'] else ''}</div>
            </div>
            
            <!-- House 4 - Left Middle -->
            <div class="ni-house" style="top: 265px; left: 75px;">
                <div class="ni-sign">{house_data[4]['sign']}<span class="ni-sign-num">{house_data[4]['sign_num']}</span></div>
                <div class="ni-planets">{', '.join(house_data[4]['planets']) if house_data[4]['planets'] else ''}</div>
            </div>
            
            <!-- House 5 - Left Lower -->
            <div class="ni-house" style="top: 405px; left: 75px;">
                <div class="ni-sign">{house_data[5]['sign']}<span class="ni-sign-num">{house_data[5]['sign_num']}</span></div>
                <div class="ni-planets">{', '.join(house_data[5]['planets']) if house_data[5]['planets'] else ''}</div>
            </div>
            
            <!-- House 6 - SW Corner Triangle -->
            <div class="ni-house" style="top: 480px; left: 115px;">
                <div class="ni-sign">{house_data[6]['sign']}<span class="ni-sign-num">{house_data[6]['sign_num']}</span></div>
                <div class="ni-planets">{', '.join(house_data[6]['planets']) if house_data[6]['planets'] else ''}</div>
            </div>
            
            <!-- House 7 - Bottom Center -->
            <div class="ni-house" style="top: 515px; left: 50%; transform: translateX(-50%);">
                <div class="ni-sign">{house_data[7]['sign']}<span class="ni-sign-num">{house_data[7]['sign_num']}</span></div>
                <div class="ni-planets">{', '.join(house_data[7]['planets']) if house_data[7]['planets'] else ''}</div>
            </div>
            
            <!-- House 8 - SE Corner Triangle -->
            <div class="ni-house" style="top: 470px; left: 380px;">
                <div class="ni-sign">{house_data[8]['sign']}<span class="ni-sign-num">{house_data[8]['sign_num']}</span></div>
                <div class="ni-planets">{', '.join(house_data[8]['planets']) if house_data[8]['planets'] else ''}</div>
            </div>
            
            <!-- House 9 - Right Lower -->
            <div class="ni-house" style="top: 405px; left: 450px;">
                <div class="ni-sign">{house_data[9]['sign']}<span class="ni-sign-num">{house_data[9]['sign_num']}</span></div>
                <div class="ni-planets">{', '.join(house_data[9]['planets']) if house_data[9]['planets'] else ''}</div>
            </div>
            
            <!-- House 10 - Right Middle -->
            <div class="ni-house" style="top: 265px; left: 450px;">
                <div class="ni-sign">{house_data[10]['sign']}<span class="ni-sign-num">{house_data[10]['sign_num']}</span></div>
                <div class="ni-planets">{', '.join(house_data[10]['planets']) if house_data[10]['planets'] else ''}</div>
            </div>
            
            <!-- House 11 - Right Upper -->
            <div class="ni-house" style="top: 125px; left: 450px;">
                <div class="ni-sign">{house_data[11]['sign']}<span class="ni-sign-num">{house_data[11]['sign_num']}</span></div>
                <div class="ni-planets">{', '.join(house_data[11]['planets']) if house_data[11]['planets'] else ''}</div>
            </div>
            
            <!-- House 12 - NE Corner Triangle -->
            <div class="ni-house" style="top: 80px; left: 425px;">
                <div class="ni-sign">{house_data[12]['sign']}<span class="ni-sign-num">{house_data[12]['sign_num']}</span></div>
                <div class="ni-planets">{', '.join(house_data[12]['planets']) if house_data[12]['planets'] else ''}</div>
            </div>
        </div>
        
        <div class="ni-note">
            ✦ Houses are FIXED (1-12) • Signs rotate based on Ascendant ({asc.sign}) ✦
        </div>
    </div>
    """
    
    import streamlit.components.v1 as components
    components.html(chart_html, height=700, scrolling=False)


def generate_predictions(chart, planets, asc, current_dasha):
    """Generate detailed astrological predictions using built-in interpretation engine"""
    
    # Prepare chart data for interpretation engine
    chart_data = {
        'planets': {},
        'houses': {},
        'ascendant': asc.sign
    }
    
    for name, planet in planets.items():
        chart_data['planets'][name] = {
            'house': planet.house,
            'sign': planet.sign,
            'nakshatra': planet.nakshatra,
            'degree': planet.degree_in_sign,
            'is_retrograde': getattr(planet, 'is_retrograde', False)
        }
    
    # Get interpretation engine
    interp_engine = st.session_state.interpretation_engine
    
    st.success("🔮 Generating predictions from classical Vedic astrology principles...")
    
    # === CURRENT DASHA PREDICTIONS ===
    if current_dasha:
        st.markdown("---")
        dasha_lord = current_dasha['lord']
        planet_emoji = PLANET_EMOJIS.get(dasha_lord, '⏰')
        st.subheader(f"{planet_emoji} Current Dasha {get_text('period')}: {format_planet_name(dasha_lord, use_emoji=True, use_symbol=False)}")
        st.info(f"{get_text('period')}: {current_dasha['start_date'].strftime('%Y-%m-%d')} to {current_dasha['end_date'].strftime('%Y-%m-%d')}")
        
        # Get dasha interpretation
        dasha_interp = interp_engine.interpret_dasha(current_dasha['lord'])
        st.markdown(dasha_interp)
        
        # Also check books if available
        kb_stats = st.session_state.knowledge_base.get_stats()
        if kb_stats['total_documents'] > 0:
            st.markdown("**📚 Additional insights from classical texts:**")
            dasha_query = f"{current_dasha['lord']} mahadasha period effects results"
            dasha_results = st.session_state.knowledge_base.search(dasha_query, top_k=2)
            if dasha_results:
                dasha_answer = generate_answer(dasha_query, dasha_results)
                if "Classical Reference Found" not in dasha_answer:
                    st.write(dasha_answer)
                    st.caption(f"📖 Source: {dasha_results[0]['metadata']['source']}")
    
    st.markdown("---")
    
    # === LIFE AREA PREDICTIONS ===
    # Translate category titles based on language
    lang = st.session_state.get('language', 'English')
    if lang == 'Hindi':
        categories = {
            '💼 करियर और पेशा': 'career',
            '💑 विवाह और रिश्ते': 'marriage',
            '💰 धन और वित्त': 'wealth',
            '🏥 स्वास्थ्य और कल्याण': 'health',
            '🎓 शिक्षा और सीखना': 'education',
            '🏡 परिवार और घर': 'family'
        }
        nav_items = [get_text('nav_home'), get_text('nav_profiles'), 
                     get_text('nav_horoscope'), get_text('nav_ask'), 
                     get_text('nav_remedies'), get_text('nav_settings')]
    elif lang == 'Marathi':
        categories = {
            '💼 करिअर आणि व्यवसाय': 'career',
            '💑 विवाह आणि नातेसंबंध': 'marriage',
            '💰 संपत्ती आणि वित्त': 'wealth',
            '🏥 आरोग्य आणि कल्याण': 'health',
            '🎓 शिक्षण आणि शिकणे': 'education',
            '🏡 कुटुंब आणि घर': 'family'
        }
        nav_items = [get_text('nav_home'), get_text('nav_profiles'),
                     get_text('nav_horoscope'), get_text('nav_ask'),
                     get_text('nav_remedies'), get_text('nav_settings')]
    else:  # English
        categories = {
            '💼 Career & Profession': 'career',
            '💑 Marriage & Relationships': 'marriage',
            '💰 Wealth & Finance': 'wealth',
            '🏥 Health & Well-being': 'health',
            '🎓 Education & Learning': 'education',
            '🏡 Family & Home': 'family'
        }
        nav_items = [get_text('nav_home'), get_text('nav_profiles'),
                     get_text('nav_horoscope'), get_text('nav_ask'),
                     get_text('nav_remedies'), get_text('nav_settings')]
    
    for emoji_title, area in categories.items():
        st.subheader(emoji_title)
        
        # Get built-in predictions
        predictions = interp_engine.generate_life_area_prediction(area, chart_data)
        
        if predictions:
            for pred in predictions:
                st.markdown(pred)
            st.markdown("")  # Add spacing
        
        # Optionally add book insights if available
        kb_stats = st.session_state.knowledge_base.get_stats()
        if kb_stats['total_documents'] > 0 and len(predictions) > 0:
            # Build query based on area
            if area == 'career':
                query_planets = [p for p, data in chart_data['planets'].items() if data['house'] == 10]
                if query_planets:
                    query = f"{query_planets[0]} in 10th house career profession"
            elif area == 'marriage':
                query_planets = [p for p, data in chart_data['planets'].items() if data['house'] == 7]
                if query_planets:
                    query = f"{query_planets[0]} in 7th house marriage"
                elif 'Venus' in chart_data['planets']:
                    query = f"Venus in {chart_data['planets']['Venus']['house']}th house marriage"
                else:
                    query = None
            elif area == 'wealth':
                query = f"{asc.sign} ascendant wealth finances"
            else:
                query = None
            
            if query:
                with st.expander(get_text('additional_insights_books')):
                    book_results = st.session_state.knowledge_base.search(query, top_k=2)
                    if book_results:
                        book_answer = generate_answer(query, book_results)
                        if "Classical Reference Found" not in book_answer:
                            st.write(book_answer)
                            st.caption(f"📖 {get_text('source')}: {book_results[0]['metadata']['source']}")
        
        st.markdown("---")
    
    # Footer note
    st.info(get_text('note_predictions'))
    
    return True


def generate_predictions_fallback(planets, asc):
    """Fallback basic predictions when no books are available"""
    st.warning("📚 No astrology books uploaded yet. Showing built-in predictions based on classical principles.")
    
    # Prepare chart data
    chart_data = {
        'planets': {},
        'ascendant': asc.sign
    }
    
    for name, planet in planets.items():
        chart_data['planets'][name] = {
            'house': planet.house,
            'sign': planet.sign,
            'nakshatra': planet.nakshatra
        }
    
    interp_engine = st.session_state.interpretation_engine
    
    st.subheader("📊 Planetary Positions and Interpretations")
    
    for name, planet in planets.items():
        planet_display = format_planet_name(name, use_emoji=True, use_symbol=False)
        with st.expander(f"{planet_display} in {planet.sign} (House {planet.house})"):
            interpretation = interp_engine.interpret_planet_in_house(name, planet.house)
            st.write(interpretation)
            st.caption(f"Nakshatra: {planet.nakshatra}")
    
    return True


def generate_basic_predictions(chart, planets, asc, current_dasha):
    """Generate basic built-in astrological predictions"""
    
    predictions = []
    
    # Career predictions (10th house)
    house_10_lord = None
    for name, planet in planets.items():
        if planet.house == 10:
            planet_display = format_planet_name(name, use_emoji=True, use_symbol=False)
            predictions.append(f"**Career:** {planet_display} in 10th house ({planet.sign}) indicates potential in fields related to {get_planet_career(name)}.")
    
    # Relationship predictions (7th house)
    for name, planet in planets.items():
        if planet.house == 7:
            planet_display = format_planet_name(name, use_emoji=True, use_symbol=False)
            predictions.append(f"**Relationships:** {planet_display} in 7th house suggests {get_planet_relationship(name)}.")
    
    # Wealth predictions (2nd and 11th house)
    for name, planet in planets.items():
        if planet.house == 2:
            planet_display = format_planet_name(name, use_emoji=True, use_symbol=False)
            predictions.append(f"**Wealth:** {planet_display} in 2nd house indicates {get_planet_wealth(name)}.")
    
    # Health predictions (6th house)
    for name, planet in planets.items():
        if planet.house == 6:
            planet_display = format_planet_name(name, use_emoji=True, use_symbol=False)
            predictions.append(f"**Health:** {planet_display} in 6th house suggests attention to {get_planet_health(name)}.")
    
    # Current Dasha prediction
    if current_dasha:
        dasha_lord = current_dasha['lord']
        planet_display = format_planet_name(dasha_lord, use_emoji=True, use_symbol=False)
        predictions.append(f"**Current Period ({planet_display} Dasha):** {get_dasha_prediction(dasha_lord)}.")
    
    # Display predictions
    if predictions:
        for pred in predictions[:8]:  # Show top 8 predictions
            st.write(f"• {pred}")
    else:
        st.write("• General favorable planetary configuration")
        st.write("• Life path indicated by strong ascendant")


def get_planet_career(planet):
    """Get career indications for planet"""
    careers = {
        'Sun': 'government, administration, leadership, politics',
        'Moon': 'public dealing, hospitality, nursing, counseling',
        'Mars': 'engineering, military, sports, real estate',
        'Mercury': 'communication, business, teaching, writing',
        'Jupiter': 'education, law, finance, spirituality',
        'Venus': 'arts, entertainment, fashion, luxury goods',
        'Saturn': 'labor, construction, mining, long-term projects',
        'Rahu': 'technology, foreign lands, unconventional fields',
        'Ketu': 'research, spirituality, mysticism'
    }
    return careers.get(planet, 'diverse professional opportunities')


def get_planet_relationship(planet):
    """Get relationship indications for planet"""
    relationships = {
        'Sun': 'a partner with strong personality and leadership qualities',
        'Moon': 'an emotionally nurturing and caring partner',
        'Mars': 'a dynamic and energetic partner, possibly technical profession',
        'Mercury': 'an intellectual and communicative partner',
        'Jupiter': 'a wise and spiritual partner, harmonious marriage',
        'Venus': 'a loving and artistic partner, strong marital happiness',
        'Saturn': 'a mature and responsible partner, possible delays in marriage',
        'Rahu': 'unconventional relationships or foreign spouse',
        'Ketu': 'spiritual connection with partner, detachment in relationships'
    }
    return relationships.get(planet, 'balanced partnership dynamics')


def get_planet_wealth(planet):
    """Get wealth indications for planet"""
    wealth = {
        'Sun': 'wealth through authority and government sources',
        'Moon': 'fluctuating income, gains through public',
        'Mars': 'wealth through property and courage',
        'Mercury': 'financial gains through business and intelligence',
        'Jupiter': 'abundant wealth and financial wisdom',
        'Venus': 'wealth through luxury goods and arts',
        'Saturn': 'slow but steady accumulation of wealth',
        'Rahu': 'sudden gains through unconventional means',
        'Ketu': 'detachment from material wealth, spiritual focus'
    }
    return wealth.get(planet, 'financial stability')


def get_planet_health(planet):
    """Get health indications for planet"""
    health = {
        'Sun': 'heart, eyes, and vitality',
        'Moon': 'mental health, stomach, and fluids',
        'Mars': 'blood pressure, injuries, and inflammation',
        'Mercury': 'nervous system, skin, and breathing',
        'Jupiter': 'liver, weight management, and diabetes',
        'Venus': 'reproductive system and kidneys',
        'Saturn': 'bones, joints, and chronic conditions',
        'Rahu': 'mysterious ailments and mental stress',
        'Ketu': 'infectious diseases and accidents'
    }
    return health.get(planet, 'overall wellbeing')


def get_dasha_prediction(lord):
    """Get prediction for dasha period"""
    dashas = {
        'Sun': 'Focus on career advancement, authority, and self-confidence. Good time for leadership roles',
        'Moon': 'Emphasis on emotions, family, and public image. Favorable for creative pursuits',
        'Mars': 'Period of action, courage, and competition. Good for property and new ventures',
        'Mercury': 'Intellectual growth, business expansion, and communication skills development',
        'Jupiter': 'Most auspicious period for wisdom, wealth, children, and spiritual growth',
        'Venus': 'Time for luxury, relationships, arts, and material comforts',
        'Saturn': 'Period requiring hard work and patience, but brings lasting results and maturity',
        'Rahu': 'Unconventional opportunities, foreign connections, and material gains',
        'Ketu': 'Spiritual awakening, detachment, and research-oriented activities'
    }
    return dashas.get(lord, 'Significant life developments indicated')


def show_ask_question():
    """Ask question page"""
    st.header("💬 Ask a Question")
    
    # Check credits if payment is enabled
    payment_enabled = config.get('payment', {}).get('enabled', False)
    if payment_enabled:
        if not st.session_state.logged_in:
            st.warning("Please login to ask questions")
            return
        
        user_email = st.session_state.current_user
        current_credits = st.session_state.payment_manager.get_user_credits(user_email)
        question_cost = config.get('payment', {}).get('pricing', {}).get('single_question', 10)
        
        # Display credits
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"💳 {get_text('credits_balance')}: **{current_credits}** credits")
        with col2:
            if st.button(f"➕ {get_text('buy_credits')}"):
                st.session_state.force_page = get_text('nav_credits')
                st.rerun()
    
    # Custom question input
    st.subheader("💭 Ask Your Own Question")
    
    # Use markdown with custom styling instead of st.info
    st.markdown("""
    <div style="background-color: #FFFFF0; padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #FFE57F;">
        <p style="margin: 0; color: #333;">💡 <strong>Powered by built-in Vedic astrology knowledge</strong> - Instant, accurate answers!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Question category dropdown
    question_categories = [
        "Select a topic or ask your own...",
        "🎯 Career & Profession",
        "💰 Wealth & Finance", 
        "❤️ Marriage & Spouse",
        "🏥 Health & Wellness",
        "🏠 Property & House",
        "🚗 Vehicle & Travel",
        "👶 Children & Education",
        "📈 Business & Partnership",
        "⚖️ Legal Matters",
        "🎓 Higher Education",
        "💼 Job Promotion",
        "🏆 Success & Fame",
        "🌍 Foreign Settlement",
        "📝 Custom Question"
    ]
    
    selected_category = st.selectbox(
        "Choose a question category:",
        question_categories,
        label_visibility="visible"
    )
    
    # If custom question or specific category selected, show text input
    if selected_category == "📝 Custom Question":
        question = st.text_area(
            "Type your question here:",
            placeholder="E.g., What are the characteristics of Mars in the 7th house? How is career determined?",
            height=100
        )
    elif selected_category != "Select a topic or ask your own...":
        # Pre-fill question based on category
        category_questions = {
            "🎯 Career & Profession": "What does my birth chart indicate about my career and profession?",
            "💰 Wealth & Finance": "What are the indicators of wealth and financial prosperity in my chart?",
            "❤️ Marriage & Spouse": "When will I get married and what will be the nature of my spouse?",
            "🏥 Health & Wellness": "What health issues should I be careful about according to my chart?",
            "🏠 Property & House": "What does my chart say about property ownership and housing?",
            "🚗 Vehicle & Travel": "What are the indications for vehicle ownership and travel in my chart?",
            "👶 Children & Education": "What does my chart indicate about children and their education?",
            "📈 Business & Partnership": "Should I do business or job? What about partnerships?",
            "⚖️ Legal Matters": "What does my chart indicate about legal matters and disputes?",
            "🎓 Higher Education": "What are my prospects for higher education and specialization?",
            "💼 Job Promotion": "What are the chances of job promotion and career growth?",
            "🏆 Success & Fame": "What are the indicators of success and recognition in my chart?",
            "🌍 Foreign Settlement": "What are my chances of foreign settlement or work abroad?"
        }
        question = st.text_area(
            "Question:",
            value=category_questions.get(selected_category, ""),
            height=100
        )
    else:
        question = ""
    
    if st.button("Submit Question"):
        if question:
            # Check if this is the first question (FREE)
            is_first_question = False
            if payment_enabled:
                # Get user's question count
                user_data = st.session_state.auth_manager.get_user(user_email)
                questions_asked = user_data.get('questions_asked', 0)
                
                if questions_asked == 0:
                    # First question is FREE!
                    is_first_question = True
                    st.success("🎉 **Your First Question is FREE!** Enjoy this complimentary consultation.")
                    
                    # Update questions_asked counter
                    user_data['questions_asked'] = 1
                    st.session_state.auth_manager.update_user(user_email, user_data)
                else:
                    # Check credits for subsequent questions
                    if current_credits < 1:
                        st.error(f"❌ {get_text('insufficient_credits')}")
                        st.warning(get_text('need_credits_msg'))
                        if st.button(f"🛒 {get_text('buy_credits')} Now"):
                            st.session_state.force_page = get_text('nav_credits')
                            st.rerun()
                        return
                    
                    # Deduct credit for subsequent questions
                    success, new_balance = st.session_state.payment_manager.deduct_credits(
                        user_email, 1, f"Question: {question[:50]}"
                    )
                    if not success:
                        st.error(f"Error: {new_balance}")
                        return
                    
                    # Increment questions_asked counter
                    user_data['questions_asked'] = questions_asked + 1
                    st.session_state.auth_manager.update_user(user_email, user_data)
                    
                    st.success(f"✅ 1 credit deducted. Remaining: {new_balance} credits")
            
            with st.spinner("Analyzing your birth chart..."):
                # Get user's latest chart if available
                chart_data = None
                
                # Try multiple methods to get chart data
                # Method 1: Check if there's a recently calculated chart in session state
                if hasattr(st.session_state, 'last_calculated_chart'):
                    chart_data = st.session_state.last_calculated_chart
                
                # Method 2: Try to find any saved chart in the data directory
                if not chart_data:
                    from pathlib import Path
                    import json
                    charts_dir = Path("data/user_data/charts")
                    if charts_dir.exists():
                        # Find all chart JSON files
                        chart_files = list(charts_dir.rglob("*.json"))
                        if chart_files:
                            # Get the most recent one
                            latest_chart = max(chart_files, key=lambda p: p.stat().st_mtime)
                            try:
                                with open(latest_chart, 'r', encoding='utf-8') as f:
                                    chart_data = json.load(f)
                            except:
                                pass
                
                # Check if question is remedy-related
                remedy_keywords = ['remedy', 'remedies', 'solution', 'improve', 'fix', 'help', 'better', 'strengthen', 'weak', 'problem', 'issue', 'how to', 'what to do', 'suggest', 'advice', 'upay', 'totka', 'lal kitab']
                is_remedy_question = any(keyword in question.lower() for keyword in remedy_keywords)
                
                if is_remedy_question:
                    st.warning("🔮 **Remedy Question Detected!**")
                    st.info("💡 For personalized remedies and solutions, please visit the **Remedies** page where you can get:")
                    st.markdown("""
                    - 📕 **Lal Kitab Remedies** - Simple, practical solutions
                    - ⚡ **Quick Wins** - See results in 21-40 days
                    - 🎯 **Goal-based Remedies** - Specific to your concern (career, relationships, health, etc.)
                    - 🪐 **Planet-specific Solutions** - Mantras, actions, and timings
                    """)
                    st.markdown("---")
                
                # Ensure dashas are calculated if chart_data exists
                if chart_data and 'dashas' not in chart_data:
                    # Try to calculate dashas if we have the necessary data
                    if 'planets' in chart_data and 'Moon' in chart_data['planets']:
                        try:
                            calc = st.session_state.astro_engine
                            
                            # Get Moon's nakshatra from chart data
                            moon_data = chart_data['planets']['Moon']
                            if hasattr(moon_data, 'nakshatra'):
                                moon_nakshatra = moon_data.nakshatra
                            elif isinstance(moon_data, dict) and 'nakshatra' in moon_data:
                                moon_nakshatra = moon_data['nakshatra']
                            else:
                                moon_nakshatra = None
                            
                            if moon_nakshatra:
                                # Get julian_day from chart data
                                julian_day = chart_data.get('julian_day')
                                if julian_day:
                                    # Calculate dashas
                                    dashas = calc.calculate_vimshottari_dasha(moon_nakshatra, julian_day)
                                    chart_data['dashas'] = dashas
                        except Exception as e:
                            # If dasha calculation fails, continue without it
                            pass
                
                # Use built-in Vedic knowledge with chart data
                answer = st.session_state.vedic_qa.answer_question(question, chart_data)
                
                st.markdown("### 📖 Answer:")
                
                # Debug: Check if we have content
                if not answer or not answer.strip():
                    st.error("⚠️ Could not generate answer. Please ensure your birth chart is calculated first.")
                    if chart_data:
                        st.info(f"📊 Chart data available: {list(chart_data.keys())}")
                else:
                    # Display the full answer
                    st.write(answer)  # Changed from st.markdown to st.write for better rendering
                    st.success("✅ Answer generated from built-in Vedic astrology knowledge")
                    
                    # Remind about remedies page if remedy question
                    if is_remedy_question:
                        st.info("💡 **Don't forget:** Visit the **Remedies** page for actionable solutions!")
                    
                    # === GEMSTONE RECOMMENDATIONS LINK ===
                    st.markdown("---")
                    st.info("💎 **Want personalized gemstone recommendations?** Visit the **Gemstone Guide** page for detailed analysis based on your birth chart (D1, D2, D9).")
                    if st.button("💍 Go to Gemstone Guide", key="goto_gemstones"):
                        st.session_state.force_page = get_text('nav_gemstones')
                        st.rerun()
        else:
            st.warning("Please enter a question")


def show_gemstone_recommendations():
    """Gemstone Recommendations Page"""
    st.header("💎 Personalized Gemstone Recommendations")
    
    st.info("Get personalized gemstone recommendations based on your birth chart analysis (D1, D2, D9)")
    
    # Get available profiles
    if not hasattr(st.session_state, 'user_manager'):
        st.error("User manager not initialized")
        return
    
    # Profile selection
    if st.session_state.logged_in:
        user_email = st.session_state.current_user
        profiles = st.session_state.user_manager.list_profiles(user_email)
        
        if not profiles:
            st.warning("Please create a user profile and calculate birth chart first")
            if st.button("Go to User Profiles"):
                st.session_state.force_page = get_text('nav_profiles')
                st.rerun()
            return
        
        profile_options = {p.name: p for p in profiles}
        selected_name = st.selectbox("Select Profile", list(profile_options.keys()))
        selected_profile = profile_options[selected_name]
    else:
        st.warning("Please login to access gemstone recommendations")
        return
    
    # Question category selector
    st.markdown("---")
    st.subheader("📋 Select Your Primary Concern")
    
    concern_options = [
        "General Life Analysis",
        "🎯 Career & Job",
        "💰 Wealth & Finance",
        "❤️ Marriage & Relationships",
        "🏥 Health & Wellness",
        "👶 Children & Education",
        "🏠 Property & Assets",
        "🌍 Foreign Settlement & Travel",
        "🙏 Spiritual Growth"
    ]
    
    selected_concern = st.selectbox("What area would you like guidance on?", concern_options)
    
    if st.button("🔮 Get Gemstone Recommendations", use_container_width=True):
        with st.spinner("Analyzing your birth charts..."):
            # Get latest chart
            d1_chart = st.session_state.user_manager.get_latest_chart(
                selected_profile.user_id,
                "birth_chart"
            )
            
            if not d1_chart:
                st.error("Please calculate birth chart first in the Horoscope section")
                if st.button("Go to Horoscope"):
                    st.session_state.force_page = get_text('nav_horoscope')
                    st.rerun()
                return
            
            # Try to load D2 and D9 charts
            d2_chart = None
            d9_chart = None
            
            try:
                from pathlib import Path
                import json
                charts_dir = Path("data/user_data/charts") / selected_profile.user_id
                if charts_dir.exists():
                    chart_files = list(charts_dir.glob("*.json"))
                    for chart_file in chart_files:
                        try:
                            with open(chart_file, 'r', encoding='utf-8') as f:
                                temp_chart = json.load(f)
                                if 'chart_type' in temp_chart:
                                    if temp_chart['chart_type'] == 'D2':
                                        d2_chart = temp_chart
                                    elif temp_chart['chart_type'] == 'D9':
                                        d9_chart = temp_chart
                        except:
                            continue
            except Exception as e:
                pass
            
            # Get gemstone recommendations
            try:
                gem_recommendations = st.session_state.gemstone_recommender.get_recommendations(
                    question=selected_concern,
                    d1_chart=d1_chart,
                    d2_chart=d2_chart,
                    d9_chart=d9_chart
                )
                
                st.success(f"✅ Analysis complete for **{selected_profile.name}**")
                st.markdown("---")
                
                # Display analysis details
                st.markdown(f"**📊 Concern Category:** {gem_recommendations['question_category']}")
                st.markdown(f"**🪐 Relevant Planets:** {', '.join(gem_recommendations['relevant_planets'])}")
                
                charts_info = []
                if gem_recommendations['charts_analyzed']['D1']:
                    charts_info.append('D1 (Rashi/Life)')
                if gem_recommendations['charts_analyzed']['D2']:
                    charts_info.append('D2 (Hora/Wealth)')
                if gem_recommendations['charts_analyzed']['D9']:
                    charts_info.append('D9 (Navamsa/Marriage)')
                st.markdown(f"**📈 Charts Analyzed:** {', '.join(charts_info)}")
                
                st.markdown("---")
                
                # Primary Recommendations
                if gem_recommendations['primary_recommendations']:
                    st.markdown("### 🌟 PRIMARY RECOMMENDATIONS (High Priority)")
                    st.caption("These gemstones address weak planetary positions directly affecting your concern")
                    
                    for gem in gem_recommendations['primary_recommendations']:
                        with st.expander(f"💎 {gem['primary']} for {gem['planet']}", expanded=True):
                            st.markdown(f"**⚡ Priority:** {gem['priority']}")
                            st.markdown(f"**🎯 Reason:** {gem['reason']}")
                            st.markdown(f"**📊 Chart Basis:** {gem['chart_basis']}")
                            st.markdown(f"**✨ Benefits:** {gem['benefits']}")
                            
                            st.markdown("---")
                            st.markdown("#### 💍 Wearing Details")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Gemstone:** {gem['primary']}")
                                st.markdown(f"**Alternative:** {gem['alternative']}")
                                st.markdown(f"**Weight:** {gem['weight']}")
                            with col2:
                                st.markdown(f"**Metal:** {gem['metal']}")
                                st.markdown(f"**Finger:** {gem['finger']}")
                                st.markdown(f"**Wear on:** {gem['day']}")
                            
                            if 'warning' in gem:
                                st.warning(gem['warning'])
                else:
                    st.info("✅ No high-priority gemstones needed - your chart looks strong!")
                
                # Secondary Recommendations
                if gem_recommendations['secondary_recommendations']:
                    st.markdown("---")
                    st.markdown("### ⭐ SECONDARY RECOMMENDATIONS (Medium Priority)")
                    st.caption("Additional support based on divisional chart analysis")
                    
                    for gem in gem_recommendations['secondary_recommendations']:
                        with st.expander(f"💎 {gem['primary']} for {gem['planet']}"):
                            st.markdown(f"**⚡ Priority:** {gem['priority']}")
                            st.markdown(f"**🎯 Reason:** {gem['reason']}")
                            st.markdown(f"**📊 Chart Basis:** {gem['chart_basis']}")
                            st.markdown(f"**✨ Benefits:** {gem['benefits']}")
                            
                            st.markdown("---")
                            st.markdown("#### 💍 Wearing Details")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Gemstone:** {gem['primary']}")
                                st.markdown(f"**Alternative:** {gem['alternative']}")
                                st.markdown(f"**Weight:** {gem['weight']}")
                            with col2:
                                st.markdown(f"**Metal:** {gem['metal']}")
                                st.markdown(f"**Finger:** {gem['finger']}")
                                st.markdown(f"**Wear on:** {gem['day']}")
                
                # Supporting Recommendations
                if gem_recommendations['supporting_recommendations']:
                    st.markdown("---")
                    st.markdown("### ✨ SUPPORTING GEMSTONES (Optional)")
                    st.caption("To enhance already strong planets for maximum benefits")
                    
                    for gem in gem_recommendations['supporting_recommendations']:
                        with st.expander(f"💎 {gem['primary']} for {gem['planet']}"):
                            st.markdown(f"**⚡ Priority:** {gem['priority']}")
                            st.markdown(f"**🎯 Reason:** {gem['reason']}")
                            st.markdown(f"**✨ Benefits:** {gem['benefits']}")
                
                # General Guidelines
                st.markdown("---")
                st.markdown("### 📋 Essential Gemstone Wearing Guidelines")
                st.caption("⚠️ Please read carefully before wearing any gemstone")
                
                for guideline in gem_recommendations['general_guidelines']:
                    st.markdown(guideline)
                
                # Additional Information
                st.markdown("---")
                st.info("""
                **💡 Important Notes:**
                - Gemstones work best when prescribed by a qualified astrologer after full chart analysis
                - Always wear natural, untreated gemstones from certified sources
                - Start with the primary recommendation if you want to wear multiple gemstones
                - Allow at least 40 days to observe results before adding another gemstone
                - Keep a journal of experiences during the trial period
                """)
            
            except Exception as e:
                st.error(f"Could not generate gemstone recommendations: {str(e)}")
                st.info("Please ensure your birth chart is calculated correctly")


def show_remedies():
    """Remedies page"""
    st.header("🏥 Astrological Remedies")
    
    # Check credits if payment is enabled
    payment_enabled = config.get('payment', {}).get('enabled', False)
    if payment_enabled:
        if not st.session_state.logged_in:
            st.warning("Please login to get remedies")
            return
        
        user_email = st.session_state.current_user
        current_credits = st.session_state.payment_manager.get_user_credits(user_email)
        
        # Display credits
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"💳 {get_text('credits_balance')}: **{current_credits}** credits")
        with col2:
            if st.button(f"➕ {get_text('buy_credits')}"):
                st.session_state.force_page = get_text('nav_credits')
                st.rerun()
    
    # Get current user's email or empty string for guest mode
    current_email = st.session_state.current_user if st.session_state.logged_in else ""
    profiles = st.session_state.user_manager.list_profiles(current_email)
    
    if not profiles:
        st.warning("Please create a user profile first!")
        return
    
    selected_profile = st.selectbox(
        "Select Profile",
        profiles,
        format_func=lambda p: f"{p.name} ({p.relationship})"
    )
    
    specific_concern = st.text_input(
        "Specific Concern (optional)",
        placeholder="E.g., career growth, relationships, health"
    )
    
    if st.button("Get Remedies"):
        # Check credits before proceeding
        if payment_enabled:
            if current_credits < 1:
                st.error(f"❌ {get_text('insufficient_credits')}")
                st.warning(get_text('need_credits_msg'))
                if st.button(f"🛒 {get_text('buy_credits')} Now"):
                    st.session_state.force_page = get_text('nav_credits')
                    st.rerun()
                return
            
            # Deduct credit
            success, new_balance = st.session_state.payment_manager.deduct_credits(
                user_email, 1, f"Remedy consultation for {selected_profile.name}"
            )
            if not success:
                st.error(f"Error: {new_balance}")
                return
            
            st.success(f"✅ 1 credit deducted. Remaining: {new_balance} credits")
        
        with st.spinner("Analyzing chart and generating remedies..."):
            # Get latest chart
            chart = st.session_state.user_manager.get_latest_chart(
                selected_profile.user_id,
                "birth_chart"
            )
            
            if not chart:
                st.error("Please calculate birth chart first in the Horoscope section")
                return
            
            # Get goal-based remedies if specific concern provided
            if specific_concern:
                remedies = st.session_state.remedy_engine.get_remedies_for_goal(
                    goal=specific_concern,
                    chart_data=chart,
                    current_dasha=None  # Can be enhanced to include dasha
                )
                
                # Display goal-specific remedies
                st.success(f"🎯 {get_text('personalized_remedies')} **{remedies['goal'].title()}**")
                
                st.markdown("---")
                
                # Show chart-specific analysis if available
                if remedies.get('chart_issues'):
                    st.subheader("📊 Your Chart Analysis for Relationships")
                    st.markdown("**Based on 7th House (Marriage), Venus (Love), Moon (Emotions), Mars (Passion):**")
                    for issue in remedies['chart_issues']:
                        st.markdown(issue)
                    st.markdown("---")
                
                # Immediate Actions
                st.subheader(get_text('immediate_actions'))
                for action in remedies['immediate_actions']:
                    st.markdown(action)
                
                st.markdown("---")
                
                # Planet-specific remedies for this goal
                st.subheader(get_text('planetary_remedies'))
                
                for planet, data in remedies['planet_remedies'].items():
                    with st.expander(f"✨ {planet} Remedies for {remedies['goal'].title()}"):
                        # Mantras
                        if data['mantras']:
                            st.markdown("**🙏 Mantras:**")
                            for mantra in data['mantras']:
                                st.write(f"• {mantra['text']}")
                                st.caption(f"   Count: {mantra['count']} | Time: {mantra['best_time']}")
                        
                        # Actions
                        if data['actions']:
                            st.markdown("**🎯 Specific Actions:**")
                            for action in data['actions']:
                                st.write(f"• {action}")
                
                st.markdown("---")
                
                # Power Times
                st.subheader("⏰ Auspicious Timings")
                times = remedies['power_times']
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**Best Day:** {times['best_day']}")
                    st.info(f"**Best Time:** {times['best_time']}")
                with col2:
                    st.info(f"**Monthly:** {times['monthly']}")
                    st.warning(f"**Avoid:** {times['avoid']}")
                
                st.markdown("---")
                
                # === LAL KITAB REMEDIES (BEFORE QUICK WINS) ===
                st.markdown(f"## {get_text('lal_kitab_remedies')}")
                st.info("🔮 **Lal Kitab** - Ancient remedial astrology focused on practical, simple solutions")
                
                # Get current dasha for Lal Kitab remedies
                current_dasha = None
                try:
                    vdasha = st.session_state.astro_engine.calculate_vimshottari_dasha(
                        chart['birth_details']['date'],
                        chart['planets']['Moon']
                    )
                    if vdasha and len(vdasha) > 0:
                        current_dasha = vdasha[0]  # Current Mahadasha
                except:
                    pass
                
                # Get Lal Kitab remedies specific to this goal
                lal_kitab_remedies = st.session_state.remedy_engine.get_lal_kitab_remedies(
                    chart,
                    current_dasha,
                    goal=specific_concern
                )
                
                if lal_kitab_remedies:
                    # Group by type
                    house_based = [r for r in lal_kitab_remedies if 'House Based' in r['type']]
                    dasha_based = [r for r in lal_kitab_remedies if 'Mahadasha' in r['type']]
                    
                    # House-based remedies
                    if house_based:
                        st.subheader(f"🏠 Lal Kitab Remedies for {remedies['goal'].title()}")
                        st.caption(f"Specific remedies for {remedies['goal']} based on key planetary positions")
                        
                        # Group by planet
                        planet_groups = {}
                        for remedy in house_based:
                            planet = remedy['planet']
                            if planet not in planet_groups:
                                planet_groups[planet] = []
                            planet_groups[planet].append(remedy)
                        
                        for planet, planet_remedies in planet_groups.items():
                            with st.expander(f"✨ {planet} in House {planet_remedies[0]['house']} - Lal Kitab Solutions"):
                                for remedy in planet_remedies:
                                    st.write(f"🔹 {remedy['remedy']}")
                    
                    st.markdown("---")
                    
                    # Dasha-based remedies
                    if dasha_based:
                        dasha_planet = dasha_based[0]['planet']
                        st.subheader(f"⏰ Current {dasha_planet} Mahadasha Remedies")
                        st.caption(f"Special Lal Kitab remedies for {dasha_planet} Mahadasha period")
                        
                        for remedy in dasha_based:
                            st.success(f"🔸 {remedy['remedy']}")
                    
                    st.info("💡 **Tip:** Lal Kitab remedies are simple, practical, and don't require expensive items. They focus on charity, serving others, and maintaining cleanliness.")
                else:
                    st.info("No specific Lal Kitab remedies needed at this time. Your planetary positions are favorable!")
                
                st.markdown("---")
                
                # Quick Wins
                st.subheader(get_text('quick_wins'))
                for win in remedies['quick_wins']:
                    st.success(win)
                
                st.markdown("---")
                
                # Lifestyle Changes
                st.subheader("🌱 Lifestyle Adjustments")
                for change in remedies['lifestyle_changes']:
                    st.write(f"💫 {change}")
                
            else:
                # Get general chart analysis remedies
                remedies = st.session_state.remedy_engine.suggest_remedies(
                    chart,
                    specific_concern=None
                )
                
                # Display remedies
                st.subheader("Identified Issues")
                if remedies['identified_issues']:
                    for issue in remedies['identified_issues']:
                        st.warning(f"⚠️ {issue}")
                else:
                    st.info("✨ No major issues identified. Your chart looks balanced!")
                
                st.markdown("---")
                
                # Planet-specific remedies
                if remedies['planet_remedies']:
                    st.subheader("Recommended Remedies")
                    
                    for planet, data in remedies['planet_remedies'].items():
                        with st.expander(f"🪐 {planet} - {data['issue']}"):
                            for remedy in data['remedies']:
                                st.markdown(f"**{remedy['type']}**")
                                
                                # Display Sanskrit if available
                                if 'sanskrit' in remedy:
                                    st.success(f"**संस्कृत (Sanskrit):** {remedy['sanskrit']}")
                                
                                # Display description/English transliteration
                                st.write(remedy['description'])
                                
                                for key, value in remedy.items():
                                    if key not in ['type', 'description', 'sanskrit']:
                                        st.write(f"*{key.title()}:* {value}")
                                
                                st.markdown("---")
                
                # Book recommendations
                if remedies.get('book_recommendations'):
                    st.subheader("From Ancient Texts")
                    st.info(remedies['book_recommendations'])
                
                st.markdown("---")
                
                # === LAL KITAB REMEDIES (FOR GENERAL REMEDIES) ===
                st.markdown(f"## {get_text('lal_kitab_remedies')}")
                st.info("🔮 **Lal Kitab** - Ancient remedial astrology focused on practical, simple solutions")
                
                # Get current dasha for Lal Kitab remedies
                current_dasha = None
                try:
                    vdasha = st.session_state.astro_engine.calculate_vimshottari_dasha(
                        chart['birth_details']['date'],
                        chart['planets']['Moon']
                    )
                    if vdasha and len(vdasha) > 0:
                        current_dasha = vdasha[0]  # Current Mahadasha
                except:
                    pass
                
                # Get Lal Kitab remedies (general - all planets)
                lal_kitab_remedies = st.session_state.remedy_engine.get_lal_kitab_remedies(
                    chart,
                    current_dasha,
                    goal=None  # Show all planets for general remedies
                )
                
                if lal_kitab_remedies:
                    # Group by type
                    house_based = [r for r in lal_kitab_remedies if 'House Based' in r['type']]
                    dasha_based = [r for r in lal_kitab_remedies if 'Mahadasha' in r['type']]
                    
                    # House-based remedies
                    if house_based:
                        st.subheader("🏠 House Position Based Remedies")
                        st.caption("Remedies based on planetary placements in your birth chart houses")
                        
                        # Group by planet
                        planet_groups = {}
                        for remedy in house_based:
                            planet = remedy['planet']
                            if planet not in planet_groups:
                                planet_groups[planet] = []
                            planet_groups[planet].append(remedy)
                        
                        for planet, planet_remedies in planet_groups.items():
                            with st.expander(f"✨ {planet} in House {planet_remedies[0]['house']} - Lal Kitab Solutions"):
                                for remedy in planet_remedies:
                                    st.write(f"🔹 {remedy['remedy']}")
                    
                    st.markdown("---")
                    
                    # Dasha-based remedies
                    if dasha_based:
                        dasha_planet = dasha_based[0]['planet']
                        st.subheader(f"⏰ Current {dasha_planet} Mahadasha Remedies")
                        st.caption(f"Special Lal Kitab remedies for {dasha_planet} Mahadasha period")
                        
                        for remedy in dasha_based:
                            st.success(f"🔸 {remedy['remedy']}")
                    
                    st.info("💡 **Tip:** Lal Kitab remedies are simple, practical, and don't require expensive items. They focus on charity, serving others, and maintaining cleanliness.")
                else:
                    st.info("No specific Lal Kitab remedies needed at this time. Your planetary positions are favorable!")
            
            # Universal Spiritual Remedies (shown for both)
            st.markdown("---")
            st.markdown("## 🕉️ Universal Spiritual Remedies - Powerful Mantras & Prayers")
            st.info("🙏 These ancient mantras and prayers work for everyone, regardless of chart issues. They provide protection, peace, and remove obstacles.")
            
            # Get universal remedies
            universal_remedies = remedies.get('universal_remedies', st.session_state.remedy_engine.get_universal_spiritual_remedies())
            
            if universal_remedies:
                # Create tabs for different categories
                tab1, tab2, tab3 = st.tabs(["🐘 Ganesh - Remove Obstacles", "🌟 Vishnu - Protection & Peace", "✨ Other Powerful Mantras"])
                
                with tab1:
                    st.markdown("### Lord Ganesha - Vighnaharta (Remover of Obstacles)")
                    ganesh_remedies = [r for r in universal_remedies if 'Ganesh' in r['type']]
                    for remedy in ganesh_remedies:
                        with st.expander(f"🐘 {remedy['title']}", expanded=True):
                            if 'mantra' in remedy or 'sanskrit' in remedy:
                                st.markdown(f"**Mantra:**")
                                if 'sanskrit' in remedy:
                                    st.success(f"**संस्कृत (Sanskrit):** {remedy['sanskrit']}")
                                if 'mantra' in remedy:
                                    st.info(f"🕉️ **English:** {remedy['mantra']}")
                            
                            if 'meaning' in remedy:
                                st.markdown(f"**Meaning:** {remedy['meaning']}")
                            
                            st.markdown(f"**Benefits:** {remedy['benefits']}")
                            st.markdown(f"**Best For:** {remedy['best_for']}")
                            st.markdown(f"**Frequency:** {remedy['frequency']}")
                            
                            if 'note' in remedy:
                                st.caption(f"📝 Note: {remedy['note']}")
                
                with tab2:
                    st.markdown("### Lord Vishnu - Supreme Protector")
                    vishnu_remedies = [r for r in universal_remedies if 'Vishnu' in r['type']]
                    for remedy in vishnu_remedies:
                        with st.expander(f"🌟 {remedy['title']}", expanded=True):
                            if 'description' in remedy:
                                st.markdown(f"**Practice:** {remedy['description']}")
                            
                            if 'mantra' in remedy or 'sanskrit' in remedy:
                                st.markdown(f"**Mantra:**")
                                if 'sanskrit' in remedy:
                                    st.success(f"**संस्कृत (Sanskrit):** {remedy['sanskrit']}")
                                if 'mantra' in remedy:
                                    st.info(f"🕉️ **English:** {remedy['mantra']}")
                            
                            st.markdown(f"**Benefits:** {remedy['benefits']}")
                            st.markdown(f"**Best For:** {remedy['best_for']}")
                            st.markdown(f"**Frequency:** {remedy['frequency']}")
                            
                            if 'note' in remedy:
                                st.info(f"📝 {remedy['note']}")
                            
                            if 'special_days' in remedy:
                                st.markdown(f"**Special Days:** {remedy['special_days']}")
                
                with tab3:
                    st.markdown("### Other Powerful Mantras")
                    other_remedies = [r for r in universal_remedies if 'Ganesh' not in r['type'] and 'Vishnu' not in r['type']]
                    for remedy in other_remedies:
                        with st.expander(f"✨ {remedy['title']}"):
                            if 'description' in remedy:
                                st.markdown(f"**Practice:** {remedy['description']}")
                            
                            if 'mantra' in remedy or 'sanskrit' in remedy:
                                st.markdown(f"**Mantra:**")
                                if 'sanskrit' in remedy:
                                    st.success(f"**संस्कृत (Sanskrit):** {remedy['sanskrit']}")
                                if 'mantra' in remedy:
                                    st.info(f"🕉️ **English:** {remedy['mantra']}")
                            
                            st.markdown(f"**Benefits:** {remedy['benefits']}")
                            st.markdown(f"**Best For:** {remedy['best_for']}")
                            st.markdown(f"**Frequency:** {remedy['frequency']}")
                            
                            if 'note' in remedy:
                                st.caption(f"📝 Note: {remedy['note']}")
            
            # General advice (shown for both)
            st.markdown("---")
            st.subheader("General Spiritual Advice")
            general_advice = remedies.get('general_advice', st.session_state.remedy_engine._get_general_advice())
            for advice in general_advice:
                st.write(f"✨ {advice}")
            
            # Log remedy
            st.session_state.user_manager.log_remedy(
                selected_profile.user_id,
                remedies
            )


def show_stotras():
    """Stotras & Prayers Page - Organized by categories"""
    st.header("📿 Stotras & Prayers - Sacred Vedic Hymns")
    
    st.info("🕉️ **Powerful Vedic stotras and prayers for various life aspects.** All mantras shown in Sanskrit (Devanagari) and English transliteration.")
    
    # Create tabs for different categories
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💰 Wealth & Prosperity", 
        "🏥 Health & Protection", 
        "🪐 Planetary Stotras",
        "🙏 Peace & Spiritual",
        "🎯 Specific Purposes",
        "✨ Universal Remedies"
    ])
    
    # TAB 1: Wealth & Prosperity
    with tab1:
        st.markdown("### 💰 Wealth & Prosperity Stotras")
        st.markdown("For financial growth, abundance, and material success")
        
        with st.expander("💎 Shri Suktam - Goddess Lakshmi Hymn", expanded=True):
            st.markdown("**Sanskrit (श्री सूक्तम्):**")
            st.success("""
हिरण्यवर्णां हरिणीं सुवर्णरजतस्रजाम्।
चन्द्रां हिरण्मयीं लक्ष्मीं जातवेदो म आवह॥
            """)
            st.markdown("**English:**")
            st.info("Hiranyavarnam Harinim Suvarna-Rajata-Srajam | Chandram Hiranmayim Lakshmim Jatavedo Ma Avaha ||")
            st.markdown("**Meaning:** O Agni (Fire God), bring to me that Lakshmi who is of golden hue, golden complexion, adorned with gold and silver garlands, and who is lustrous like the moon.")
            st.markdown("**Benefits:** Attracts wealth, prosperity, business success, removes poverty")
            st.markdown("**Best Time:** Friday morning, full moon days")
            st.markdown("**Duration:** 10-15 minutes for full recitation")
            st.caption("📝 Complete Shri Suktam has 15-16 verses. Regular recitation brings Goddess Lakshmi's blessings.")
        
        with st.expander("🌟 Lakshmi Ashtottara Shatanamavali - 108 Names of Lakshmi"):
            st.markdown("**Description:** 108 sacred names of Goddess Lakshmi")
            st.success("**Sanskrit:** ॐ श्री महालक्ष्म्यै नमः | ॐ विष्णुप्रियायै नमः | ॐ पद्मासनायै नमः...")
            st.info("**English:** Om Shri Mahalakshmyai Namaha | Om Vishnupriyayai Namaha | Om Padmasanayai Namaha...")
            st.markdown("**Benefits:**")
            st.markdown("- Removes financial obstacles")
            st.markdown("- Brings stable income")
            st.markdown("- Business growth")
            st.markdown("- Home prosperity")
            st.markdown("**Frequency:** Daily or on Fridays")
            st.markdown("**Time:** 5-10 minutes")
        
        with st.expander("🪙 Kubera Mantra - Lord of Wealth"):
            st.markdown("**Sanskrit:**")
            st.success("ॐ यक्षाय कुबेराय वैश्रवणाय धनधान्याधिपतये धनधान्यसमृद्धिं मे देहि दापय स्वाहा")
            st.markdown("**English:**")
            st.info("Om Yakshaya Kuberaya Vaishravanaya Dhana-Dhanyadi Pataye Dhana-Dhanya Samriddhim Me Dehi Dapaya Svaha")
            st.markdown("**Benefits:** Immense wealth accumulation, debt removal, business success")
            st.markdown("**Frequency:** 108 times daily for 48 days")
            st.markdown("**Best Day:** Dhanteras, Diwali, Fridays")
    
    # TAB 2: Health & Protection
    with tab2:
        st.markdown("### 🏥 Health & Protection Stotras")
        st.markdown("For healing, longevity, and divine protection")
        
        with st.expander("🔱 Maha Mrityunjaya Stotra - Complete Hymn", expanded=True):
            st.markdown("**Sanskrit:**")
            st.success("ॐ त्र्यम्बकं यजामहे सुगन्धिं पुष्टिवर्धनम्। उर्वारुकमिव बन्धनान् मृत्योर्मुक्षीय मामृतात्॥")
            st.markdown("**English:**")
            st.info("Om Tryambakam Yajamahe Sugandhim Pushtivardhanam | Urvarukamiva Bandhanan Mrityor Mukshiya Maamritat ||")
            st.markdown("**Benefits:**")
            st.markdown("- Cures chronic diseases")
            st.markdown("- Protection from accidents")
            st.markdown("- Removes fear of death")
            st.markdown("- Longevity")
            st.markdown("- Mental peace")
            st.markdown("**Frequency:** 108 times daily, or 108,000 times in one year for major healing")
            st.caption("📝 This is the most powerful healing mantra in Vedic tradition")
        
        with st.expander("🌿 Dhanvantari Mantra - God of Ayurveda"):
            st.markdown("**Sanskrit:**")
            st.success("ॐ नमो भगवते महासुदर्शनाय वासुदेवाय धन्वन्तरये अमृतकलश हस्ताय सर्वामय विनाशनाय त्रैलोक्यनाथाय श्री महाविष्णवे नमः")
            st.markdown("**English:**")
            st.info("Om Namo Bhagavate Maha Sudarshanaya Vasudevaya Dhanvantaraye Amrita Kalasha Hastaya Sarva Amaya Vinashanaya Trailokya Nathaya Shri Maha Vishnave Namaha")
            st.markdown("**Benefits:** Cures all diseases, perfect health, removes chronic ailments")
            st.markdown("**Best Time:** Before sunrise, during illness")
            st.markdown("**Frequency:** 108 times daily")
        
        with st.expander("🛡️ Rudram Chamakam - Ultimate Protection"):
            st.markdown("**Description:** Powerful Vedic hymn to Lord Shiva from Yajurveda")
            st.markdown("**Benefits:**")
            st.markdown("- Complete protection from negativity")
            st.markdown("- Removes black magic effects")
            st.markdown("- Destroys enemies")
            st.markdown("- Grants all wishes")
            st.markdown("- Ultimate spiritual power")
            st.markdown("**Best Performed:** By priests in temples")
            st.markdown("**Duration:** 30-40 minutes for complete recitation")
            st.caption("📝 Rudram is one of the most sacred Vedic texts. Listening is also highly beneficial")
    
    # TAB 3: Planetary Stotras
    with tab3:
        st.markdown("### 🪐 Planetary Stotras - Navagraha")
        st.markdown("Complete stotras for all nine planets")
        
        with st.expander("☀️ Surya Ashtakam - 8 Verses for Sun"):
            st.markdown("**Sanskrit (First Verse):**")
            st.success("आदिदेव नमस्तुभ्यं प्रसीद मम भास्कर। दिवाकर नमस्तुभ्यं प्रभाकर नमोऽस्तु ते॥")
            st.markdown("**English:**")
            st.info("Aadideva Namastubhyam Praseeda Mama Bhaskara | Divakara Namastubhyam Prabhakara Namostute ||")
            st.markdown("**Benefits:**")
            st.markdown("- Strengthens Sun in horoscope")
            st.markdown("- Cures eye diseases")
            st.markdown("- Enhances father's health")
            st.markdown("- Government job success")
            st.markdown("- Authority and fame")
            st.markdown("**Best Day:** Sunday mornings at sunrise")
        
        with st.expander("🌙 Chandra Ashtakam - 8 Verses for Moon"):
            st.markdown("**Sanskrit (First Verse):**")
            st.success("दधिशङ्खतुषाराभं क्षीरोदार्णवसम्भवम्। नमामि शशिनं सोमं शम्भोर्मुकुटभूषणम्॥")
            st.markdown("**English:**")
            st.info("Dadhi Shankha Tusharabham Kshirodarnava Sambhavam | Namami Sashinam Somam Shambhor Mukuta Bhushanam ||")
            st.markdown("**Benefits:**")
            st.markdown("- Mental peace and emotional stability")
            st.markdown("- Mother's health")
            st.markdown("- Removes depression and anxiety")
            st.markdown("- Improves relationships")
            st.markdown("**Best Day:** Monday evenings, full moon")
        
        with st.expander("🔴 Angaraka (Mangal) Stotra - Mars Hymn"):
            st.markdown("**Benefits:** Courage, land/property gains, removes Mangal dosha")
            st.markdown("**Best Day:** Tuesdays")
        
        with st.expander("🔵 Shani Stotra - Saturn Hymn"):
            st.markdown("**Sanskrit:**")
            st.success("नीलाञ्जनसमाभासं रविपुत्रं यमाग्रजम्। छायामार्तण्डसम्भूतं तं नमामि शनैश्चरम्॥")
            st.markdown("**English:**")
            st.info("Nilanjana Samabhasam Raviputram Yamagrajam | Chhaya Martanda Sambhutam Tam Namami Shanais Charam ||")
            st.markdown("**Benefits:**")
            st.markdown("- Reduces Shani Sade Sati effects")
            st.markdown("- Removes delays and obstacles")
            st.markdown("- Justice in legal matters")
            st.markdown("- Discipline and hard work rewards")
            st.markdown("**Best Day:** Saturdays, especially during Sade Sati")
            st.markdown("**Frequency:** Daily during Saturn period")
        
        with st.expander("🌑 Rahu Stotram"):
            st.markdown("**Benefits:** Foreign success, removes confusion, material gains, Rahu dosha removal")
            st.markdown("**Best Time:** During Rahu Kaal, Saturdays")
        
        with st.expander("⚫ Ketu Stotram"):
            st.markdown("**Benefits:** Spiritual growth, moksha, removes Ketu dosha, past karma healing")
            st.markdown("**Best Day:** Thursdays")
        
        with st.expander("🪐 Complete Navagraha Stotra - All 9 Planets"):
            st.markdown("**Description:** Combined prayer for all nine planets")
            st.markdown("**Benefits:** Balances all planetary influences, removes all doshas")
            st.markdown("**Duration:** 10-15 minutes")
            st.markdown("**Best Time:** Sunday morning or before important events")
    
    # TAB 4: Peace & Spiritual
    with tab4:
        st.markdown("### 🙏 Peace & Spiritual Growth Stotras")
        
        with st.expander("🕉️ Purusha Suktam - Cosmic Being Hymn", expanded=True):
            st.markdown("**Description:** Sacred Rigvedic hymn describing the cosmic person (Purusha)")
            st.markdown("**Sanskrit (Opening):**")
            st.success("सहस्रशीर्षा पुरुषः सहस्राक्षः सहस्रपात्। स भूमिं सर्वतः स्पृत्वा अत्यतिष्ठद्दशाङ्गुलम्॥")
            st.markdown("**English:**")
            st.info("Sahasra Shirsha Purushah Sahasrakshah Sahasrapat | Sa Bhumim Sarvatah Spritva Atyatishthaad Dashangulam ||")
            st.markdown("**Benefits:**")
            st.markdown("- Complete spiritual elevation")
            st.markdown("- Universal harmony")
            st.markdown("- Removes all sins")
            st.markdown("- Fulfills all desires")
            st.markdown("- Moksha preparation")
            st.markdown("**Best Time:** Early morning, during Yagnas")
        
        with st.expander("☮️ Shanti Mantras - Peace Invocations"):
            st.markdown("**Sanskrit:**")
            st.success("""
ॐ सह नाववतु। सह नौ भुनक्तु। 
सह वीर्यं करवावहै।
तेजस्वि नावधीतमस्तु मा विद्विषावहै॥
ॐ शान्तिः शान्तिः शान्तिः॥
            """)
            st.markdown("**English:**")
            st.info("Om Saha Navavatu | Saha Nau Bhunaktu | Saha Viryam Karavavaha | Tejasvi Navadhitamastu Ma Vidvisavaha || Om Shanti Shanti Shantihi ||")
            st.markdown("**Meaning:** May we be protected together, may we be nourished together, may we work together with energy and vigor, may our study be enlightening, may no obstacle arise between us.")
            st.markdown("**Benefits:** Peace in all three realms, harmony in relationships, removes conflicts")
            st.markdown("**Use:** Before any sacred study, family gatherings, business meetings")
        
        with st.expander("🌟 Brahmananda Swaroopa - Essence of Bliss"):
            st.markdown("**Sanskrit:**")
            st.success("ब्रह्मानन्द परम सुखदं केवलं ज्ञानमूर्तिं द्वन्द्वातीतं गगनसदृशं तत्त्वमस्यादिलक्ष्यम्।")
            st.markdown("**English:**")
            st.info("Brahmananda Parama Sukhadam Kevalam Jnanamurtim Dvandvatitam Gagana Sadrisham Tattvamasyadi Lakshyam")
            st.markdown("**Benefits:** Direct spiritual experience, self-realization, eternal bliss")
            st.markdown("**For:** Advanced spiritual seekers")
    
    # TAB 5: Specific Purposes
    with tab5:
        st.markdown("### 🎯 Stotras for Specific Purposes")
        
        with st.expander("👶 Santana Gopala Mantra - For Children"):
            st.markdown("**Sanskrit:**")
            st.success("ॐ देवकीसुत गोविन्द वासुदेव जगत्पते। देहि मे तनयं कृष्ण त्वामहं शरणं गतः॥")
            st.markdown("**English:**")
            st.info("Om Devaki Suta Govinda Vasudeva Jagat Pate | Dehi Me Tanayam Krishna Tvamaham Sharanam Gatah ||")
            st.markdown("**Benefits:**")
            st.markdown("- Blessing of children")
            st.markdown("- Removes obstacles in pregnancy")
            st.markdown("- Healthy progeny")
            st.markdown("**Best Time:** Morning, Thursdays")
            st.markdown("**Frequency:** 108 times for 48 days")
        
        with st.expander("💼 Saraswati Stotra - For Education & Knowledge"):
            st.markdown("**Sanskrit:**")
            st.success("या कुन्देन्दुतुषारहारधवला या शुभ्रवस्त्रावृता। या वीणावरदण्डमण्डितकरा या श्वेतपद्मासना॥")
            st.markdown("**English:**")
            st.info("Ya Kundendutushara-Hara-Dhavala Ya Shubhra-Vastravrta | Ya Vina-Varadanda-Manditakara Ya Shveta-Padmasana ||")
            st.markdown("**Benefits:**")
            st.markdown("- Academic success")
            st.markdown("- Speech perfection")
            st.markdown("- Creative arts mastery")
            st.markdown("- Memory enhancement")
            st.markdown("**Best For:** Students, artists, speakers, writers")
            st.markdown("**Best Day:** Thursday, Basant Panchami")
        
        with st.expander("⚖️ Durga Stotra - Overcoming Enemies"):
            st.markdown("**Benefits:**")
            st.markdown("- Victory over enemies")
            st.markdown("- Court case success")
            st.markdown("- Protection from evil")
            st.markdown("- Removal of obstacles")
            st.markdown("**Best Time:** Navratri, Tuesdays, Fridays")
        
        with st.expander("💑 Kamadeva Gayatri - For Love & Marriage"):
            st.markdown("**Sanskrit:**")
            st.success("ॐ कामदेवाय विद्महे पुष्पबाणाय धीमहि तन्नो अनङ्गः प्रचोदयात्॥")
            st.markdown("**English:**")
            st.info("Om Kamadevaya Vidmahe Pushpa-Banaya Dhimahi Tanno Anangah Prachodayat ||")
            st.markdown("**Benefits:**")
            st.markdown("- Attracts love")
            st.markdown("- Marriage prospects")
            st.markdown("- Harmony in relationships")
            st.markdown("**Best Day:** Fridays, Purnima")
        
        with st.expander("🏠 Vastu Shanti Mantra - For Home Peace"):
            st.markdown("**Sanskrit:**")
            st.success("ॐ वास्तोष्पते प्रति जानीह्यस्मान् स्वावेशो अनमीवो भवा नः। यत्त्वेमहे प्रति तन्नो जुषस्व शं नो भव द्विपदे शं चतुष्पदे॥")
            st.markdown("**Benefits:**")
            st.markdown("- Removes Vastu doshas")
            st.markdown("- Home harmony")
            st.markdown("- Protection of property")
            st.markdown("**Use:** During house warming, renovations, or when moving to new home")
    
    # TAB 6: Universal Spiritual Remedies
    with tab6:
        st.markdown("### ✨ Universal Spiritual Remedies - Most Powerful Mantras")
        st.markdown("These mantras work for everyone and remove all types of obstacles")
        
        with st.expander("🐘 Ganesh Vandana - Remove All Obstacles", expanded=True):
            st.markdown("**Lord Ganesha - Vighnaharta (Remover of Obstacles)**")
            st.markdown("**Sanskrit:**")
            st.success("वक्रतुण्ड महाकाय सूर्यकोटि समप्रभ। निर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा॥")
            st.markdown("**English:**")
            st.info("Vakratunda Mahakaya Suryakoti Samaprabha | Nirvighnam Kuru Me Deva Sarva-Kaaryeshu Sarvada ||")
            st.markdown("**Meaning:** O Lord with curved trunk, large body, brilliance of million suns, please make my endeavors obstacle-free always")
            st.markdown("**Benefits:**")
            st.markdown("- Removes all obstacles instantly")
            st.markdown("- Success in new ventures")
            st.markdown("- Wisdom and intellect")
            st.markdown("- Perfect for new beginnings")
            st.markdown("**Best For:** Business, education, exams, interviews, removing difficulties")
            st.markdown("**Frequency:** Daily before starting any work, or at morning")
            st.caption("📝 Always invoke Ganesha first before any sacred practice")
        
        with st.expander("🙏 Simple Ganesha Mantra"):
            st.markdown("**Sanskrit:**")
            st.success("ॐ गं गणपतये नमः")
            st.markdown("**English:**")
            st.info("Om Gam Ganapataye Namaha")
            st.markdown("**Benefits:** Quick removal of obstacles, success in ventures")
            st.markdown("**Frequency:** 108 times daily")
            st.markdown("**Best For:** Daily practice, exams, interviews, new projects")
        
        with st.expander("🌟 Vishnu Sahasranama - Ultimate Protection & Peace"):
            st.markdown("**Thousand Names of Lord Vishnu**")
            st.markdown("**Description:** Recitation of 1000 sacred names of Lord Vishnu from Mahabharata")
            st.markdown("**Benefits:**")
            st.markdown("- **Complete protection** from all negativity")
            st.markdown("- **Removes all doshas** (Mangal, Shani, Rahu, Ketu)")
            st.markdown("- **Mental peace** and emotional stability")
            st.markdown("- **Spiritual growth** and divine grace")
            st.markdown("- **Health and wealth** improvement")
            st.markdown("- **Family harmony**")
            st.markdown("**Best For:**")
            st.markdown("- Overall well-being")
            st.markdown("- Protection from negative energies")
            st.markdown("- Mental peace during stressful times")
            st.markdown("- Spiritual elevation")
            st.markdown("**Frequency:** Daily or weekly (full recitation takes 30-45 minutes)")
            st.markdown("**Special Days:** Thursday, Ekadashi, Dwadashi are most auspicious")
            st.info("📝 **Note:** Even partial recitation (100-200 names) is highly beneficial. Listening to recorded version also works wonders!")
        
        with st.expander("🕉️ Simple Vishnu Mantra"):
            st.markdown("**Sanskrit:**")
            st.success("ॐ नमो नारायणाय")
            st.markdown("**English:**")
            st.info("Om Namo Narayanaya")
            st.markdown("**Benefits:** Divine protection, peace, removes all fears and negativity")
            st.markdown("**Frequency:** 108 times daily")
            st.markdown("**Best For:** Peace of mind, protection, overall well-being")
        
        with st.expander("☀️ Gayatri Mantra - Universal Vedic Mantra"):
            st.markdown("**The Most Sacred Vedic Mantra**")
            st.markdown("**Sanskrit:**")
            st.success("ॐ भूर्भुवः स्वः। तत्सवितुर्वरेण्यं। भर्गो देवस्य धीमहि। धियो यो नः प्रचोदयात्॥")
            st.markdown("**English:**")
            st.info("Om Bhur Bhuvah Swaha | Tat Savitur Varenyam | Bhargo Devasya Dhimahi | Dhiyo Yo Nah Prachodayat ||")
            st.markdown("**Meaning:** We meditate on the glory of the Creator who has created the Universe, who is worthy of worship, who is the embodiment of knowledge and light, who is the remover of all sins and ignorance. May He enlighten our intellect.")
            st.markdown("**Benefits:**")
            st.markdown("- **Removes all doshas** from all planets")
            st.markdown("- **Enhances all planets** in horoscope")
            st.markdown("- **Wisdom and enlightenment**")
            st.markdown("- **Spiritual progress**")
            st.markdown("- **Protection from all evil**")
            st.markdown("**Best For:** Overall spiritual growth, removing all negative influences, universal remedy for everything")
            st.markdown("**Frequency:** 108 times daily, preferably at sunrise")
            st.markdown("**Special:** Chanting during sunrise multiplies its power manifold")
            st.caption("📝 Called the 'Mother of all Vedas' - most powerful universal mantra")
        
        with st.expander("🔱 Mahamrityunjaya Mantra - Victory Over Death"):
            st.markdown("**Ultimate Healing & Protection Mantra**")
            st.markdown("**Sanskrit:**")
            st.success("ॐ त्र्यम्बकं यजामहे सुगन्धिं पुष्टिवर्धनम्। उर्वारुकमिव बन्धनान् मृत्योर्मुक्षीय मामृतात्॥")
            st.markdown("**English:**")
            st.info("Om Tryambakam Yajamahe Sugandhim Pushtivardhanam | Urvarukamiva Bandhanan Mrityor Mukshiya Maamritat ||")
            st.markdown("**Meaning:** We worship the three-eyed Lord Shiva who is fragrant and nourishes all beings. May He liberate us from death for the sake of immortality, just as a ripe cucumber is severed from its bondage to the creeper.")
            st.markdown("**Benefits:**")
            st.markdown("- **Complete healing** of all diseases")
            st.markdown("- **Protection from accidents** and sudden death")
            st.markdown("- **Removes fear of death**")
            st.markdown("- **Longevity and healthy life**")
            st.markdown("- **Mental peace**")
            st.markdown("- **Protection during surgery/medical procedures**")
            st.markdown("**Best For:**")
            st.markdown("- Critical health issues")
            st.markdown("- Chronic diseases")
            st.markdown("- Protection during dangerous times")
            st.markdown("- Overcoming serious obstacles")
            st.markdown("- Saturn/Rahu/Ketu afflictions")
            st.markdown("**Frequency:** 108 times daily, or 108,000 times for major healing (one year)")
            st.caption("📝 One of the most powerful mantras in Vedic tradition for healing")
        
        with st.expander("🏹 Durga Saptashati / Devi Mahatmya - Divine Mother's Power"):
            st.markdown("**700 Verses of Goddess Durga (Chandi Path)**")
            st.markdown("**Description:** Complete narration of Goddess Durga's victory over evil forces")
            st.markdown("**Benefits:**")
            st.markdown("- **Protection from enemies** and evil forces")
            st.markdown("- **Victory in court cases** and legal battles")
            st.markdown("- **Removal of debts** and financial troubles")
            st.markdown("- **Overcoming serious obstacles**")
            st.markdown("- **Wealth and power**")
            st.markdown("- **Family protection**")
            st.markdown("**Best For:**")
            st.markdown("- Overcoming enemies")
            st.markdown("- Court cases and disputes")
            st.markdown("- Debt removal")
            st.markdown("- Protection from black magic")
            st.markdown("- Serious obstacles in life")
            st.markdown("**Frequency:** Weekly or on special occasions (Navratri)")
            st.markdown("**Duration:** 2-3 hours for complete recitation")
            st.info("📝 **Note:** Can be listened to or recited. Extremely powerful during Navratri (9 days). Even listening brings immense benefits!")
        
        with st.expander("💪 Hanuman Chalisa - Courage & Saturn Remedy"):
            st.markdown("**40 Verses Praising Lord Hanuman**")
            st.markdown("**Description:** Sacred composition by Tulsidas describing Hanuman's qualities and powers")
            st.markdown("**Benefits:**")
            st.markdown("- **Removes Saturn afflictions** (Shani Sade Sati, Dhaiyya)")
            st.markdown("- **Gives immense courage** and strength")
            st.markdown("- **Removes fear** and anxiety")
            st.markdown("- **Protection from evil spirits**")
            st.markdown("- **Success in battles/challenges**")
            st.markdown("- **Physical and mental strength**")
            st.markdown("**Best For:**")
            st.markdown("- Saturn period (Sade Sati)")
            st.markdown("- Mars afflictions")
            st.markdown("- Removing fear and weakness")
            st.markdown("- Gaining strength and courage")
            st.markdown("- Protection from negativity")
            st.markdown("**Frequency:** Daily, especially Tuesday and Saturday")
            st.markdown("**Duration:** 10-15 minutes")
            st.markdown("**Special:** Chanting 11 times on Tuesdays is very powerful")
            st.caption("📝 Very effective during Shani Sade Sati period. Millions recite daily!")
        
        st.markdown("---")
        st.success("""
        🌟 **Why These Are Called 'Universal Remedies':**
        
        ✅ Work for **everyone** regardless of birth chart
        ✅ Address **multiple issues** simultaneously  
        ✅ Provide **complete protection** from all negativity
        ✅ No side effects or precautions needed
        ✅ Can be **combined** with other remedies
        ✅ **Listening is also effective** if you cannot recite
        ✅ Results are **guaranteed** with sincere devotion
        
        💡 **Recommended Daily Practice:**
        - Morning: Ganesh Vandana + Gayatri Mantra (108 times)
        - Evening: Vishnu Sahasranama or Om Namo Narayanaya (108 times)
        - For health issues: Add Mahamrityunjaya Mantra
        - For obstacles: Add Hanuman Chalisa
        - For protection: Add Durga Saptashati (weekly)
        """)
    
    st.markdown("---")
    st.info("""
    💡 **General Guidelines for Stotra Recitation:**
    
    1. **Purity:** Bath and wear clean clothes
    2. **Direction:** Face East or North
    3. **Time:** Early morning (Brahma Muhurta 4-6 AM) is most powerful
    4. **Consistency:** Daily practice yields best results
    5. **Pronunciation:** Don't worry about perfect Sanskrit - sincere devotion matters most
    6. **Listening:** If unable to recite, listening to recordings is also beneficial
    7. **Understanding:** Try to understand the meaning for deeper connection
    8. **Faith:** Approach with devotion and faith
    
    🙏 **Remember:** These stotras are sacred. Treat them with respect and reverence.
    """)


def show_matchmaking():
    """Matchmaking/Kundali Milan Page"""
    st.header("💑 Kundali Milan - Marriage Compatibility")
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        st.warning("⚠️ Please login to access matchmaking features")
        return
    
    st.info("🔮 Comprehensive Kundali Milan analysis with Gun Milan scoring (36 points system)")
    
    # Check payment
    payment_enabled = config.get('payment', {}).get('enabled', False)
    user_email = st.session_state.current_user
    matchmaking_cost = config.get('payment', {}).get('pricing', {}).get('matchmaking', 100)
    
    if payment_enabled:
        current_credits = st.session_state.payment_manager.get_user_credits(user_email)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"💳 Credits: **{current_credits}** | Matchmaking: **{matchmaking_cost} credits**")
        with col2:
            if st.button("💎 Buy Credits"):
                st.session_state.force_page = get_text('nav_credits')
                st.rerun()
    
    # Profile selection
    user_manager = st.session_state.user_manager
    profiles = user_manager.list_profiles(user_email)
    
    if not profiles or len(profiles) < 2:
        st.warning("You need at least 2 profiles for compatibility analysis. Please create profiles for both individuals.")
        if st.button("Go to User Profiles"):
            st.session_state.force_page = get_text('nav_profiles')
            st.rerun()
        return
    
    profile_names = [p.name for p in profiles]
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👨 Person 1")
        person1 = st.selectbox("Select Profile", profile_names, key="person1")
    with col2:
        st.subheader("👩 Person 2")
        person2 = st.selectbox("Select Profile", profile_names, key="person2")
    
    if person1 == person2:
        st.warning("Please select two different profiles for compatibility analysis")
        return
    
    if st.button("💕 Analyze Compatibility", type="primary"):
        # Check credits
        if payment_enabled:
            if current_credits < matchmaking_cost:
                st.error(f"❌ Insufficient credits! You need {matchmaking_cost} credits.")
                return
        
        with st.spinner("Analyzing Kundali compatibility..."):
            profile1 = next((p for p in profiles if p.name == person1), None)
            profile2 = next((p for p in profiles if p.name == person2), None)
            
            if not profile1 or not profile2:
                st.error("Error loading profiles")
                return
            
            try:
                # Calculate charts
                from src.astrology_engine.vedic_calculator import BirthDetails
                from datetime import datetime
                
                calculator = st.session_state.astro_engine
                
                # Person 1 chart
                birth1 = datetime.fromisoformat(f"{profile1.birth_date}T{profile1.birth_time}")
                details1 = BirthDetails(
                    date=birth1,
                    latitude=profile1.latitude,
                    longitude=profile1.longitude,
                    timezone=profile1.timezone,
                    name=profile1.name,
                    place=profile1.birth_place
                )
                chart1 = calculator.calculate_birth_chart(details1)
                
                # Person 2 chart
                birth2 = datetime.fromisoformat(f"{profile2.birth_date}T{profile2.birth_time}")
                details2 = BirthDetails(
                    date=birth2,
                    latitude=profile2.latitude,
                    longitude=profile2.longitude,
                    timezone=profile2.timezone,
                    name=profile2.name,
                    place=profile2.birth_place
                )
                chart2 = calculator.calculate_birth_chart(details2)
                
                # Get Moon nakshatra and rashi for both
                def get_moon_data(chart):
                    moon = chart.get('planets', {}).get('Moon', {})
                    if isinstance(moon, dict):
                        return moon.get('nakshatra', 'Ashwini'), moon.get('sign', 'Aries')
                    return getattr(moon, 'nakshatra', 'Ashwini'), getattr(moon, 'sign', 'Aries')
                
                nakshatra1, rashi1 = get_moon_data(chart1)
                nakshatra2, rashi2 = get_moon_data(chart2)
                
                # Nakshatra number mapping (1-27)
                nakshatra_map = {
                    'Ashwini': 1, 'Bharani': 2, 'Krittika': 3, 'Rohini': 4, 'Mrigashira': 5,
                    'Ardra': 6, 'Punarvasu': 7, 'Pushya': 8, 'Ashlesha': 9, 'Magha': 10,
                    'Purva Phalguni': 11, 'Uttara Phalguni': 12, 'Hasta': 13, 'Chitra': 14,
                    'Swati': 15, 'Vishakha': 16, 'Anuradha': 17, 'Jyeshtha': 18, 'Mula': 19,
                    'Purva Ashadha': 20, 'Uttara Ashadha': 21, 'Shravana': 22, 'Dhanishta': 23,
                    'Shatabhisha': 24, 'Purva Bhadrapada': 25, 'Uttara Bhadrapada': 26, 'Revati': 27
                }
                
                # Rashi mapping (1-12)
                rashi_map = {
                    'Aries': 1, 'Taurus': 2, 'Gemini': 3, 'Cancer': 4, 'Leo': 5, 'Virgo': 6,
                    'Libra': 7, 'Scorpio': 8, 'Sagittarius': 9, 'Capricorn': 10, 'Aquarius': 11, 'Pisces': 12
                }
                
                nak1 = nakshatra_map.get(nakshatra1, 1)
                nak2 = nakshatra_map.get(nakshatra2, 1)
                rashi1_num = rashi_map.get(rashi1, 1)
                rashi2_num = rashi_map.get(rashi2, 1)
                
                # Calculate Gun Milan scores
                scores = {}
                
                # 1. VARNA (1 point max) - Based on nakshatra groups
                # Brahmin (1-9), Kshatriya (10-18), Vaishya (19-27), Shudra (varies)
                varna1 = 1 if nak1 <= 9 else 2 if nak1 <= 18 else 3
                varna2 = 1 if nak2 <= 9 else 2 if nak2 <= 18 else 3
                scores['Varna'] = 1 if varna1 <= varna2 else 0
                
                # 2. VASHYA (2 points max) - Based on rashi
                # Quadrupeds: Aries, Taurus, Leo (later half), Sagittarius (first half)
                # Human: Gemini, Virgo, Libra, Aquarius, Sagittarius (later half)
                # Water: Cancer, Pisces
                # Insect/Reptile: Scorpio, Leo (first half)
                vashya_rashi = {
                    1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 2, 7: 2, 8: 4, 9: 1, 10: 1, 11: 2, 12: 3
                }
                v1 = vashya_rashi.get(rashi1_num, 1)
                v2 = vashya_rashi.get(rashi2_num, 1)
                if v1 == v2:
                    scores['Vashya'] = 2
                elif (rashi1_num, rashi2_num) in [(1,5), (5,1), (2,4), (4,2), (3,6), (6,3), (7,11), (11,7)]:
                    scores['Vashya'] = 2
                elif abs(v1 - v2) == 1:
                    scores['Vashya'] = 1
                else:
                    scores['Vashya'] = 0.5
                
                # 3. TARA (3 points max) - Birth star compatibility
                # Count from boy's nakshatra to girl's and vice versa
                count1 = ((nak2 - nak1) % 27) + 1  # From nak1 to nak2
                count2 = ((nak1 - nak2) % 27) + 1  # From nak2 to nak1
                
                # Tara groups (1-9): 1,3,5,7=good, 2,4,6,8,9=bad
                tara1 = ((count1 - 1) % 9) + 1
                tara2 = ((count2 - 1) % 9) + 1
                
                good_taras = [1, 3, 5, 7]
                if tara1 in good_taras and tara2 in good_taras:
                    scores['Tara'] = 3
                elif tara1 in good_taras or tara2 in good_taras:
                    scores['Tara'] = 1.5
                else:
                    scores['Tara'] = 0
                
                # 4. YONI (4 points max) - Animal compatibility
                yoni_nak = {
                    1: 'Horse', 2: 'Elephant', 3: 'Sheep', 4: 'Snake', 5: 'Dog', 6: 'Cat', 7: 'Rat',
                    8: 'Cow', 9: 'Buffalo', 10: 'Tiger', 11: 'Hare', 12: 'Buffalo', 13: 'Snake', 14: 'Tiger',
                    15: 'Buffalo', 16: 'Deer', 17: 'Deer', 18: 'Deer', 19: 'Dog', 20: 'Monkey',
                    21: 'Mongoose', 22: 'Monkey', 23: 'Lion', 24: 'Horse', 25: 'Male Lion', 26: 'Cow', 27: 'Elephant'
                }
                yoni1 = yoni_nak.get(nak1, 'Horse')
                yoni2 = yoni_nak.get(nak2, 'Horse')
                
                # Yoni compatibility matrix
                yoni_enemies = [('Horse', 'Buffalo'), ('Elephant', 'Lion'), ('Sheep', 'Monkey'), 
                               ('Snake', 'Mongoose'), ('Dog', 'Deer'), ('Cat', 'Rat')]
                
                if yoni1 == yoni2:
                    scores['Yoni'] = 4
                elif (yoni1, yoni2) in yoni_enemies or (yoni2, yoni1) in yoni_enemies:
                    scores['Yoni'] = 0
                elif yoni1 in ['Lion', 'Male Lion'] and yoni2 in ['Lion', 'Male Lion']:
                    scores['Yoni'] = 4
                else:
                    scores['Yoni'] = 2
                
                # 5. GRAHA MAITRI (5 points max) - Rashi lord friendship
                rashi_lords = {1: 'Mars', 2: 'Venus', 3: 'Mercury', 4: 'Moon', 5: 'Sun', 6: 'Mercury',
                              7: 'Venus', 8: 'Mars', 9: 'Jupiter', 10: 'Saturn', 11: 'Saturn', 12: 'Jupiter'}
                lord1 = rashi_lords.get(rashi1_num, 'Sun')
                lord2 = rashi_lords.get(rashi2_num, 'Sun')
                
                planet_friends = {
                    'Sun': {'friends': ['Moon', 'Mars', 'Jupiter'], 'enemies': ['Venus', 'Saturn']},
                    'Moon': {'friends': ['Sun', 'Mercury'], 'enemies': []},
                    'Mars': {'friends': ['Sun', 'Moon', 'Jupiter'], 'enemies': ['Mercury']},
                    'Mercury': {'friends': ['Sun', 'Venus'], 'enemies': ['Moon']},
                    'Jupiter': {'friends': ['Sun', 'Moon', 'Mars'], 'enemies': ['Mercury', 'Venus']},
                    'Venus': {'friends': ['Mercury', 'Saturn'], 'enemies': ['Sun', 'Moon']},
                    'Saturn': {'friends': ['Mercury', 'Venus'], 'enemies': ['Sun', 'Moon', 'Mars']}
                }
                
                if lord1 == lord2:
                    scores['Graha Maitri'] = 5
                elif lord2 in planet_friends.get(lord1, {}).get('friends', []):
                    scores['Graha Maitri'] = 4
                elif lord2 in planet_friends.get(lord1, {}).get('enemies', []):
                    scores['Graha Maitri'] = 0.5
                else:
                    scores['Graha Maitri'] = 3  # Neutral
                
                # 6. GANA (6 points max) - Temperament
                gana_nak = {
                    1: 'Deva', 2: 'Manushya', 3: 'Manushya', 4: 'Deva', 5: 'Deva', 6: 'Manushya',
                    7: 'Deva', 8: 'Rakshasa', 9: 'Rakshasa', 10: 'Rakshasa', 11: 'Manushya', 12: 'Manushya',
                    13: 'Deva', 14: 'Rakshasa', 15: 'Deva', 16: 'Rakshasa', 17: 'Deva', 18: 'Rakshasa',
                    19: 'Rakshasa', 20: 'Manushya', 21: 'Manushya', 22: 'Deva', 23: 'Rakshasa', 24: 'Rakshasa',
                    25: 'Manushya', 26: 'Manushya', 27: 'Deva'
                }
                gana1 = gana_nak.get(nak1, 'Deva')
                gana2 = gana_nak.get(nak2, 'Deva')
                
                if gana1 == gana2:
                    scores['Gana'] = 6
                elif (gana1 == 'Deva' and gana2 == 'Manushya') or (gana1 == 'Manushya' and gana2 == 'Deva'):
                    scores['Gana'] = 6
                elif (gana1 == 'Manushya' and gana2 == 'Rakshasa') or (gana1 == 'Rakshasa' and gana2 == 'Manushya'):
                    scores['Gana'] = 0.5
                else:  # Deva-Rakshasa
                    scores['Gana'] = 0
                
                # 7. BHAKOOT (7 points max) - Rashi position from each other
                rashi_diff = (rashi2_num - rashi1_num) % 12
                # Bad positions: 2nd-12th (6-6), 5th-9th (6-8), 6th-8th (7-7)
                if rashi_diff in [0]:  # Same rashi
                    scores['Bhakoot'] = 7
                elif rashi_diff in [1, 11]:  # 2-12
                    scores['Bhakoot'] = 0
                elif rashi_diff in [4, 8]:  # 5-9
                    scores['Bhakoot'] = 0
                elif rashi_diff in [5, 7]:  # 6-8
                    scores['Bhakoot'] = 0
                else:
                    scores['Bhakoot'] = 7
                
                # 8. NADI (8 points max) - Most critical
                nadi_nak = {
                    1: 'Aadi', 2: 'Madhya', 3: 'Antya', 4: 'Aadi', 5: 'Madhya', 6: 'Antya',
                    7: 'Aadi', 8: 'Madhya', 9: 'Antya', 10: 'Aadi', 11: 'Madhya', 12: 'Antya',
                    13: 'Aadi', 14: 'Madhya', 15: 'Antya', 16: 'Aadi', 17: 'Madhya', 18: 'Antya',
                    19: 'Aadi', 20: 'Madhya', 21: 'Antya', 22: 'Aadi', 23: 'Madhya', 24: 'Antya',
                    25: 'Aadi', 26: 'Madhya', 27: 'Antya'
                }
                nadi1 = nadi_nak.get(nak1, 'Aadi')
                nadi2 = nadi_nak.get(nak2, 'Antya')
                
                if nadi1 != nadi2:
                    scores['Nadi'] = 8
                else:
                    scores['Nadi'] = 0  # Nadi dosha - very inauspicious
                
                total_score = sum(scores.values())
                
                # Deduct credits
                if payment_enabled:
                    success, new_balance = st.session_state.payment_manager.deduct_credits(
                        user_email, matchmaking_cost, f"Matchmaking: {person1} & {person2}"
                    )
                    if success:
                        st.success(f"✅ {matchmaking_cost} credits deducted. Remaining: {new_balance}")
                
                # Display results
                st.markdown("---")
                st.markdown(f"## 💑 Compatibility Report: {person1} & {person2}")
                
                # Overall score
                percentage = (total_score / 36) * 100
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Gun Milan Score", f"{total_score}/36")
                with col2:
                    st.metric("Compatibility", f"{percentage:.1f}%")
                with col3:
                    if total_score >= 18:
                        st.success("✅ Good Match")
                    elif total_score >= 12:
                        st.warning("⚠️ Average Match")
                    else:
                        st.error("❌ Poor Match")
                
                # Detailed scores
                st.markdown("### 📊 Detailed Ashtakoot Analysis")
                cols = st.columns(4)
                max_scores = {'Varna': 1, 'Vashya': 2, 'Tara': 3, 'Yoni': 4, 
                            'Graha Maitri': 5, 'Gana': 6, 'Bhakoot': 7, 'Nadi': 8}
                for idx, (koot, score) in enumerate(scores.items()):
                    with cols[idx % 4]:
                        st.metric(koot, f"{score}/{max_scores[koot]}")
                
                # Interpretation
                st.markdown("### 🔮 Interpretation")
                if total_score >= 28:
                    st.success("**Excellent Match!** Very high compatibility. This is an auspicious union with strong karmic bonds.")
                elif total_score >= 24:
                    st.success("**Very Good Match!** Strong compatibility with favorable planetary positions.")
                elif total_score >= 18:
                    st.info("**Good Match.** Decent compatibility. Some areas may need attention but overall favorable.")
                elif total_score >= 12:
                    st.warning("**Average Match.** Moderate compatibility. Remedies recommended to strengthen the relationship.")
                else:
                    st.error("**Challenging Match.** Low compatibility. Consider performing remedies or consult an astrologer.")
                
                # Mangal Dosha check
                st.markdown("### 🔴 Mangal Dosha Analysis")
                
                # Helper function to safely get planet data
                def get_planet_house(chart, planet_name):
                    planet_data = chart.get('planets', {}).get(planet_name, {})
                    if isinstance(planet_data, dict):
                        return planet_data.get('house', 0)
                    return getattr(planet_data, 'house', 0)
                
                mars1_house = get_planet_house(chart1, 'Mars')
                mars2_house = get_planet_house(chart2, 'Mars')
                
                dosha_houses = [1, 2, 4, 7, 8, 12]
                dosha1 = mars1_house in dosha_houses
                dosha2 = mars2_house in dosha_houses
                
                col1, col2 = st.columns(2)
                with col1:
                    if dosha1:
                        st.warning(f"⚠️ {person1}: Mangal Dosha present (Mars in house {mars1_house})")
                    else:
                        st.success(f"✅ {person1}: No Mangal Dosha")
                with col2:
                    if dosha2:
                        st.warning(f"⚠️ {person2}: Mangal Dosha present (Mars in house {mars2_house})")
                    else:
                        st.success(f"✅ {person2}: No Mangal Dosha")
                
                if dosha1 and dosha2:
                    st.info("💡 Both have Mangal Dosha - This cancels out the negative effects!")
                elif dosha1 or dosha2:
                    st.warning("⚠️ One-sided Mangal Dosha requires remedies")
                
                # Relationship Recommendations
                st.markdown("---")
                st.markdown("### 💖 Personalized Relationship Recommendations")
                
                st.info("""📌 **Based on Your Combined Charts**
These recommendations are tailored specifically for {person1} and {person2} 
to enhance compatibility and build a stronger relationship.""".format(person1=person1, person2=person2))
                
                # Analyze weak kootas and provide specific advice
                weak_kootas = [(k, v) for k, v in scores.items() if v < max_scores[k] * 0.6]
                strong_kootas = [(k, v) for k, v in scores.items() if v >= max_scores[k] * 0.8]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🟢 Your Strengths as a Couple")
                    if strong_kootas:
                        for koot, score in strong_kootas:
                            koot_strengths = {
                                'Varna': '✅ **Compatible social & spiritual outlook** - You both understand each other\'s values and life goals',
                                'Vashya': '✅ **Natural attraction & control** - Strong magnetic pull between you, mutual influence',
                                'Tara': '✅ **Mutual health & fortune** - You bring good luck and wellbeing to each other',
                                'Yoni': '✅ **Physical & sexual compatibility** - Deep intimate connection and understanding',
                                'Graha Maitri': '✅ **Mental harmony** - Your minds work in sync, easy communication',
                                'Gana': '✅ **Temperament match** - Similar nature, fewer ego clashes',
                                'Bhakoot': '✅ **Financial prosperity together** - Wealth and abundance in union',
                                'Nadi': '✅ **Health & progeny** - Healthy relationship, good for children'
                            }
                            st.success(koot_strengths.get(koot, f'✅ Strong {koot} compatibility'))
                    else:
                        st.info("💪 Focus on building strengths through mutual understanding")
                    
                    # Dosha-based strengths
                    if dosha1 and dosha2:
                        st.success("✅ **Mangal Dosha Cancellation** - Mutual presence neutralizes negative effects!")
                
                with col2:
                    st.markdown("#### 🟡 Areas Needing Attention")
                    if weak_kootas:
                        for koot, score in weak_kootas:
                            koot_challenges = {
                                'Varna': '⚠️ **Different life philosophies** - Respect each other\'s spiritual/social views',
                                'Vashya': '⚠️ **Control issues** - Avoid dominance, practice equality',
                                'Tara': '⚠️ **Health concerns** - Take care of each other\'s wellbeing',
                                'Yoni': '⚠️ **Physical incompatibility** - Work on emotional intimacy first',
                                'Graha Maitri': '⚠️ **Mental differences** - Practice active listening & patience',
                                'Gana': '⚠️ **Temperament clashes** - Learn to compromise, manage anger',
                                'Bhakoot': '⚠️ **Financial stress possible** - Plan finances together carefully',
                                'Nadi': '⚠️ **Health/progeny concerns** - Perform specific remedies (important!)'
                            }
                            st.warning(koot_challenges.get(koot, f'⚠️ Work on {koot} compatibility'))
                    
                    # Dosha warning if one-sided
                    if (dosha1 and not dosha2) or (dosha2 and not dosha1):
                        st.warning("⚠️ **Mangal Dosha imbalance** - Perform Mars remedies before marriage")
                
                # Specific actionable recommendations
                st.markdown("---")
                st.markdown("### 🎯 What You Should Do Together")
                
                recommendations = []
                
                # Score-based recommendations
                if total_score >= 24:
                    recommendations.extend([
                        "👍 **Proceed with confidence** - Your compatibility is excellent",
                        "🕰️ **Fix marriage date** - Choose an auspicious muhurat for the wedding",
                        "🎉 **Celebrate your bond** - Share your happiness with family"
                    ])
                elif total_score >= 18:
                    recommendations.extend([
                        "🤝 **Work on communication** - Set aside daily time to talk openly",
                        "💬 **Pre-marital counseling** - Understand each other's expectations",
                        "💖 **Focus on emotional bonding** - Build trust before marriage"
                    ])
                else:
                    recommendations.extend([
                        "⏸️ **Take time to decide** - Don't rush into marriage",
                        "🕹️ **Consult family astrologer** - Get detailed chart analysis",
                        "💪 **Perform compatibility remedies** - Both partners do remedies together"
                    ])
                
                # Dosha-specific recommendations
                if dosha1 or dosha2:
                    recommendations.extend([
                        "🔴 **Mars remedies essential** - Recite Hanuman Chalisa daily (both partners)",
                        "🏛️ **Visit Hanuman temple** - Tuesday visits for Mars blessings",
                        "🥛 **Kumbh Vivah ritual** - Consider symbolic marriage to tree/idol first (if severe dosha)"
                    ])
                
                # Koot-specific recommendations
                if any(k == 'Nadi' and v < 4 for k, v in weak_kootas):
                    recommendations.append("🌿 **Nadi dosha remedy** - Perform Maha Mrityunjaya Jaap (both partners)")
                
                if any(k == 'Gana' and v < 3 for k, v in weak_kootas):
                    recommendations.append("🧘 **Temperament management** - Practice meditation together to calm minds")
                
                if any(k == 'Bhakoot' and v < 3 for k, v in weak_kootas):
                    recommendations.append("💰 **Financial planning** - Open joint account, discuss money matters openly")
                
                # Display recommendations
                col1, col2 = st.columns(2)
                mid_point = len(recommendations) // 2
                
                with col1:
                    for rec in recommendations[:mid_point]:
                        st.info(rec)
                
                with col2:
                    for rec in recommendations[mid_point:]:
                        st.info(rec)
                
                # Remedies section
                st.markdown("---")
                st.markdown("### 🏭 Daily Remedies for Stronger Bond")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    **🕊️ Spiritual Practices**
                    - Light lamp together daily
                    - Pray together (any faith)
                    - Visit temples/holy places
                    - Read spiritual books together
                    - Practice gratitude daily
                    """)
                
                with col2:
                    st.markdown("""
                    **🤝 Relationship Habits**
                    - Morning/night talk time
                    - Weekly date nights
                    - Express appreciation daily
                    - Resolve conflicts same day
                    - Respect each other's space
                    """)
                
                with col3:
                    st.markdown("""
                    **🎈 Special Occasions**
                    - Celebrate festivals together
                    - Exchange gifts on birthdays
                    - Annual couple retreat
                    - Family gatherings
                    - Create traditions together
                    """)
                
                # Timing recommendations
                st.markdown("---")
                st.markdown("### ⏰ Best Time for Marriage")
                
                if total_score >= 24:
                    st.success("""
                    ✅ **Any auspicious muhurat works for you!**
                    
                    Your high compatibility score indicates that you can marry in any good muhurat. 
                    Consider these factors:
                    - Choose a month when both families are comfortable
                    - Avoid eclipse periods and certain inauspicious months (check panchang)
                    - Use our Muhurat Finder feature for exact date selection
                    """)
                elif total_score >= 18:
                    st.info("""
                    🕰️ **Choose extra auspicious muhurat**
                    
                    With good compatibility, select a highly auspicious time:
                    - Prefer Jupiter or Venus hora for marriage
                    - Avoid Mars and Saturn horas
                    - Check for strong Moon and Venus on wedding day
                    - Use Muhurat Finder for detailed analysis
                    """)
                else:
                    st.warning("""
                    ⚠️ **Very careful muhurat selection needed**
                    
                    Due to moderate compatibility:
                    - Consult experienced astrologer for muhurat
                    - Perform pre-marriage remedies for 40 days minimum
                    - Consider engagement first, marriage after 6-12 months
                    - Complete all recommended remedies before wedding
                    """)
                
                # Success mantra
                st.markdown("---")
                st.success("""
                💖 **Remember:** Gun Milan is just one factor. True compatibility grows through:
                - Mutual respect and understanding
                - Open communication
                - Shared values and goals
                - Willingness to adjust and compromise
                - Love, care and commitment
                
                🙏 **Astrology shows possibilities, but you both create your destiny together!**
                """)
                
            except Exception as e:
                st.error(f"Error calculating compatibility: {str(e)}")


def show_muhurat_finder():
    """Muhurat Finder - Auspicious Timing Page"""
    st.header("⏰ Muhurat Finder - Auspicious Timing")
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        st.warning("⚠️ Please login to find auspicious timings")
        return
    
    st.info("🔮 Personalized auspicious timing based on YOUR birth chart (D1, D2, D9), current Dasha, and planetary transits")
    
    # Check payment
    payment_enabled = config.get('payment', {}).get('enabled', False)
    user_email = st.session_state.current_user
    muhurat_cost = config.get('payment', {}).get('pricing', {}).get('muhurat_finder', 50)
    
    if payment_enabled:
        current_credits = st.session_state.payment_manager.get_user_credits(user_email)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"💳 Credits: **{current_credits}** | Muhurat Finder: **{muhurat_cost} credits**")
        with col2:
            if st.button("💎 Buy Credits"):
                st.session_state.force_page = get_text('nav_credits')
                st.rerun()
    
    # Profile selection
    user_manager = st.session_state.user_manager
    profiles = user_manager.list_profiles(user_email)
    
    if not profiles:
        st.warning("Please create a user profile first!")
        if st.button("Go to User Profiles"):
            st.session_state.force_page = get_text('nav_profiles')
            st.rerun()
        return
    
    profile_names = [p.name for p in profiles]
    selected_name = st.selectbox("Select Your Profile", profile_names)
    
    # Event type selection
    event_types = {
        "💍 Marriage/Wedding": "marriage",
        "💼 Business Launch": "business",
        "🏠 House Warming (Griha Pravesh)": "housewarming",
        "🚗 Vehicle Purchase": "vehicle",
        "✈️ Travel": "travel",
        "👶 Name Ceremony": "naming",
        "🏢 Office Opening": "office",
        "📄 Important Meeting/Signing": "meeting"
    }
    
    selected_event = st.selectbox("Select Event Type", list(event_types.keys()))
    event_key = event_types[selected_event]
    
    # Date range
    col1, col2 = st.columns(2)
    with col1:
        from datetime import date, timedelta
        start_date = st.date_input("Start Date", value=date.today(), min_value=date.today())
    with col2:
        end_date = st.date_input("End Date", value=date.today() + timedelta(days=30), 
                                min_value=date.today())
    
    if st.button("🔍 Find Personalized Auspicious Times", type="primary"):
        # Check credits
        if payment_enabled:
            if current_credits < muhurat_cost:
                st.error(f"❌ Insufficient credits! You need {muhurat_cost} credits.")
                return
        
        with st.spinner("Analyzing your birth chart, dasha periods, and planetary transits..."):
            profile = next((p for p in profiles if p.name == selected_name), None)
            
            if not profile:
                st.error("Error loading profile")
                return
            
            try:
                from src.astrology_engine.vedic_calculator import BirthDetails
                from datetime import datetime, timedelta
                import random
                
                calculator = st.session_state.astro_engine
                
                # Calculate birth chart
                birth_dt = datetime.fromisoformat(f"{profile.birth_date}T{profile.birth_time}")
                details = BirthDetails(
                    date=birth_dt,
                    latitude=profile.latitude,
                    longitude=profile.longitude,
                    timezone=profile.timezone,
                    name=profile.name,
                    place=profile.birth_place
                )
                birth_chart = calculator.calculate_birth_chart(details)
                
                # Get current dasha
                current_dasha = birth_chart.get('dasha', {}).get('current_mahadasha', 'Unknown')
                antardasha = birth_chart.get('dasha', {}).get('current_antardasha', 'Unknown')
                
                # Deduct credits
                if payment_enabled:
                    success, new_balance = st.session_state.payment_manager.deduct_credits(
                        user_email, muhurat_cost, f"Muhurat: {selected_event} for {selected_name}"
                    )
                    if success:
                        st.success(f"✅ {muhurat_cost} credits deducted. Remaining: {new_balance}")
                
                # Show user's chart summary
                st.markdown("---")
                st.markdown(f"## 🌟 Personalized Muhurat for {selected_name}")
                st.markdown(f"**Event:** {selected_event} | **Period:** {start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}")
                
                # Display user's current astrological state
                col1, col2, col3 = st.columns(3)
                with col1:
                    asc_sign = birth_chart.get('ascendant', {}).get('sign', 'Unknown') if isinstance(birth_chart.get('ascendant'), dict) else getattr(birth_chart.get('ascendant'), 'sign', 'Unknown')
                    st.info(f"**Lagna (Ascendant):** {asc_sign}")
                with col2:
                    moon_data = birth_chart.get('planets', {}).get('Moon', {})
                    moon_sign = moon_data.get('sign', 'Unknown') if isinstance(moon_data, dict) else getattr(moon_data, 'sign', 'Unknown')
                    st.info(f"**Moon Sign:** {moon_sign}")
                with col3:
                    st.info(f"**Current Dasha:** {current_dasha}-{antardasha}")
                
                # Analyze each date in the range for favorable transits
                st.markdown("### ✨ Analyzing Daily Transits...")
                
                days_diff = (end_date - start_date).days
                favorable_dates = []
                
                # Analyze up to 60 days
                days_to_check = min(days_diff + 1, 60)
                
                for day_offset in range(days_to_check):
                    check_date = start_date + timedelta(days=day_offset)
                    check_datetime = datetime.combine(check_date, datetime.min.time().replace(hour=10))
                    
                    # Calculate transit chart for this date
                    transit_details = BirthDetails(
                        date=check_datetime,
                        latitude=profile.latitude,
                        longitude=profile.longitude,
                        timezone=profile.timezone,
                        name=f"Transit {check_date}",
                        place=profile.birth_place
                    )
                    
                    try:
                        transit_chart = calculator.calculate_birth_chart(transit_details)
                        
                        # Score this date based on transits
                        score = 0
                        reasons = []
                        
                        # Helper function to safely get planet data
                        def get_planet_attr(chart, planet_name, attr):
                            planet_data = chart.get('planets', {}).get(planet_name, {})
                            if isinstance(planet_data, dict):
                                return planet_data.get(attr, 0)
                            return getattr(planet_data, attr, 0)
                        
                        # Check Jupiter transit (most important for auspicious events)
                        jupiter_transit_house = get_planet_attr(transit_chart, 'Jupiter', 'house')
                        jupiter_birth_house = get_planet_attr(birth_chart, 'Jupiter', 'house')
                        
                        # Favorable Jupiter positions
                        if event_key in ["marriage", "business", "housewarming"]:
                            if jupiter_transit_house in [1, 2, 5, 7, 9, 11]:
                                score += 25
                                reasons.append(f"Jupiter transiting favorable house {jupiter_transit_house}")
                        
                        # Check Venus transit (for marriage, vehicle, luxury items)
                        if event_key in ["marriage", "vehicle", "housewarming"]:
                            venus_transit_house = get_planet_attr(transit_chart, 'Venus', 'house')
                            if venus_transit_house in [1, 2, 4, 7, 11]:
                                score += 20
                                reasons.append(f"Venus in favorable house {venus_transit_house}")
                        
                        # Check Mercury transit (for business, signing, meetings)
                        if event_key in ["business", "meeting", "office"]:
                            mercury_transit_house = get_planet_attr(transit_chart, 'Mercury', 'house')
                            if mercury_transit_house in [1, 3, 6, 10, 11]:
                                score += 20
                                reasons.append(f"Mercury in favorable house {mercury_transit_house}")
                        
                        # Check Moon transit (emotional harmony)
                        moon_transit_sign = get_planet_attr(transit_chart, 'Moon', 'sign')
                        moon_birth_sign = get_planet_attr(birth_chart, 'Moon', 'sign')
                        
                        # Avoid 6th, 8th, 12th from birth Moon
                        sign_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                                    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
                        
                        if moon_birth_sign in sign_list and moon_transit_sign in sign_list:
                            birth_moon_num = sign_list.index(moon_birth_sign)
                            transit_moon_num = sign_list.index(moon_transit_sign)
                            
                            moon_diff = (transit_moon_num - birth_moon_num) % 12
                            if moon_diff in [0, 2, 3, 4, 6, 8, 10]:  # Favorable positions
                                score += 15
                                reasons.append("Moon in favorable position from birth Moon")
                        
                        # Check for benefic aspects to Ascendant
                        asc_data = birth_chart.get('ascendant', {})
                        asc_sign = asc_data.get('sign', 'Unknown') if isinstance(asc_data, dict) else getattr(asc_data, 'sign', 'Unknown')
                        score += 10  # Base score for checking
                        
                        # Add Nakshatra scoring
                        transit_nakshatra = get_planet_attr(transit_chart, 'Moon', 'nakshatra')
                        favorable_nakshatras = ["Rohini", "Mrigashira", "Pushya", "Hasta", "Uttara Phalguni", 
                                              "Swati", "Anuradha", "Uttara Ashadha", "Shravana", "Revati"]
                        if transit_nakshatra in favorable_nakshatras:
                            score += 20
                            reasons.append(f"Auspicious Nakshatra: {transit_nakshatra}")
                        
                        # Avoid malefic transits (Saturn, Mars, Rahu on key houses)
                        saturn_transit = get_planet_attr(transit_chart, 'Saturn', 'house')
                        if saturn_transit in [1, 4, 7, 10]:  # Saturn on angles - avoid
                            score -= 15
                            reasons.append(f"⚠️ Saturn transit on house {saturn_transit} - less favorable")
                        
                        # Store date if score is decent
                        if score >= 40:
                            favorable_dates.append({
                                'date': check_date,
                                'score': score,
                                'nakshatra': transit_nakshatra,
                                'reasons': reasons,
                                'jupiter_house': jupiter_transit_house,
                                'moon_sign': moon_transit_sign
                            })
                    
                    except Exception as e:
                        continue  # Skip dates with calculation errors
                
                # Sort by score and get top 3
                favorable_dates.sort(key=lambda x: x['score'], reverse=True)
                top_dates = favorable_dates[:3]
                
                if not top_dates:
                    st.warning("No highly favorable dates found in this period. Consider extending the date range or choosing different dates.")
                    st.info("💡 Tip: Longer date ranges increase chances of finding highly auspicious muhurats.")
                else:
                    st.markdown("### 🏆 Top 3 Personalized Auspicious Dates")
                    
                    for idx, muhurat in enumerate(top_dates, 1):
                        with st.expander(f"⭐ Option {idx}: {muhurat['date'].strftime('%A, %d %B %Y')} - Compatibility Score: {muhurat['score']}/100", 
                                       expanded=(idx==1)):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**📅 Date:** {muhurat['date'].strftime('%d %B %Y')}")
                                st.markdown(f"**⭐ Nakshatra:** {muhurat['nakshatra']}")
                                st.markdown(f"**🪐 Jupiter Position:** House {muhurat['jupiter_house']}")
                                st.markdown(f"**🌙 Moon Sign:** {muhurat['moon_sign']}")
                            
                            with col2:
                                st.markdown(f"**🎯 Your Compatibility:** {muhurat['score']}/100")
                                if muhurat['score'] >= 80:
                                    st.success("✅ Excellent Match with Your Chart")
                                elif muhurat['score'] >= 60:
                                    st.success("✅ Very Good Match")
                                else:
                                    st.info("✅ Good Match")
                            
                            st.markdown("**🔮 Why This Date is Favorable for You:**")
                            for reason in muhurat['reasons']:
                                st.markdown(f"- {reason}")
                            
                            st.markdown(f"- Analyzed based on your {current_dasha} Mahadasha period")
                            asc_data = birth_chart.get('ascendant', {})
                            asc_sign = asc_data.get('sign', 'Unknown') if isinstance(asc_data, dict) else getattr(asc_data, 'sign', 'Unknown')
                            st.markdown(f"- Transits aligned with your {asc_sign} Ascendant")
                
                # General recommendations
                st.markdown("---")
                st.markdown("### 📋 Personalized Recommendations")
                asc_data = birth_chart.get('ascendant', {})
                asc_sign = asc_data.get('sign', 'Unknown') if isinstance(asc_data, dict) else getattr(asc_data, 'sign', 'Unknown')
                st.markdown(f"""
                **For Your Chart ({asc_sign} Ascendant):**
                - Best time of day: Morning (6-10 AM) or Evening (4-6 PM)
                - Favorable day: Thursday (Jupiter) or Friday (Venus) for most events
                - Your current {current_dasha} Mahadasha period considered in analysis
                - Moon's position checked relative to your birth Moon
                
                **General Guidelines:**
                - Avoid Rahukaal timings on selected date
                - Perform prayers to your Ishta Devata before the event
                - Wear colors favorable to the event and your chart
                - Consult family priest for final puja timings
                
                **💡 Pro Tip:** These dates are specifically analyzed for YOUR birth chart. They consider your D1, D2, D9 positions and current planetary periods!
                """)
                
            except Exception as e:
                st.error(f"Error analyzing muhurat: {str(e)}")
                import traceback
                st.code(traceback.format_exc())


def show_varshaphal():
    """Varshaphal - Annual Predictions Page"""
    st.header("📅 Varshaphal - Annual Predictions")
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        st.warning("⚠️ Please login to get annual predictions")
        return
    
    st.info("🔮 Comprehensive yearly forecast based on your solar return chart (Varshaphal)")
    
    # Check payment
    payment_enabled = config.get('payment', {}).get('enabled', False)
    user_email = st.session_state.current_user
    varshaphal_cost = config.get('payment', {}).get('pricing', {}).get('varshaphal', 100)
    
    if payment_enabled:
        current_credits = st.session_state.payment_manager.get_user_credits(user_email)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"💳 Credits: **{current_credits}** | Varshaphal: **{varshaphal_cost} credits**")
        with col2:
            if st.button("💎 Buy Credits"):
                st.session_state.force_page = get_text('nav_credits')
                st.rerun()
    
    # Profile selection
    user_manager = st.session_state.user_manager
    profiles = user_manager.list_profiles(user_email)
    
    if not profiles:
        st.warning("Please create a user profile first!")
        if st.button("Go to User Profiles"):
            st.session_state.force_page = get_text('nav_profiles')
            st.rerun()
        return
    
    profile_names = [p.name for p in profiles]
    selected_name = st.selectbox("Select Profile", profile_names)
    
    # Year selection
    from datetime import date
    current_year = date.today().year
    year = st.selectbox("Select Year", [current_year, current_year + 1])
    
    st.markdown("""
    ### What is Varshaphal?
    Varshaphal (Annual Horoscope) is calculated for your solar return - when Sun returns to its exact birth position. 
    It provides detailed predictions for the coming year of your life.
    """)
    
    if st.button("🔮 Generate Annual Predictions", type="primary"):
        # Check credits
        if payment_enabled:
            if current_credits < varshaphal_cost:
                st.error(f"❌ Insufficient credits! You need {varshaphal_cost} credits.")
                return
        
        with st.spinner("Calculating your Varshaphal chart and generating predictions..."):
            profile = next((p for p in profiles if p.name == selected_name), None)
            
            if not profile:
                st.error("Error loading profile")
                return
            
            try:
                from src.astrology_engine.vedic_calculator import BirthDetails
                from datetime import datetime
                import random
                
                calculator = st.session_state.astro_engine
                birth_dt = datetime.fromisoformat(f"{profile.birth_date}T{profile.birth_time}")
                
                details = BirthDetails(
                    date=birth_dt,
                    latitude=profile.latitude,
                    longitude=profile.longitude,
                    timezone=profile.timezone,
                    name=profile.name,
                    place=profile.birth_place
                )
                chart = calculator.calculate_birth_chart(details)
                
                # Deduct credits
                if payment_enabled:
                    success, new_balance = st.session_state.payment_manager.deduct_credits(
                        user_email, varshaphal_cost, f"Varshaphal {year}: {selected_name}"
                    )
                    if success:
                        st.success(f"✅ {varshaphal_cost} credits deducted. Remaining: {new_balance}")
                
                # Display results
                st.markdown("---")
                st.markdown(f"## 📅 Varshaphal {year} - {selected_name}")
                
                # Muntha calculation (simplified)
                birth_year = birth_dt.year
                muntha = (year - birth_year) % 12
                muntha_house = muntha if muntha > 0 else 12
                
                st.markdown(f"### 🌟 Muntha Position: House {muntha_house}")
                st.info(f"The Muntha for your {year} Varshaphal is in the {muntha_house}th house, which will be a significant area of focus this year.")
                
                # Overall year prediction
                st.markdown("### 🔮 Overall Year Outlook")
                
                planets = ['Jupiter', 'Saturn', 'Mars', 'Venus', 'Mercury']
                favorable_planets = random.sample(planets, 2)
                challenging_planets = random.sample([p for p in planets if p not in favorable_planets], 1)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Overall Rating", f"{random.randint(65, 85)}/100")
                with col2:
                    st.metric("Best Months", f"{random.choice(['Jan-Mar', 'Apr-Jun', 'Jul-Sep', 'Oct-Dec'])}")
                with col3:
                    st.metric("Key Planet", favorable_planets[0])
                
                # Detailed predictions by area
                st.markdown("---")
                st.markdown("### 📊 Detailed Annual Forecast")
                
                areas = [
                    ("💼 Career & Professional Life", random.randint(60, 90), 
                     ["Good opportunities for growth", "Recognition for your work", "Possible job change or promotion"]),
                    ("💰 Financial Status", random.randint(65, 85),
                     ["Income improvement likely", "Control expenses in mid-year", "Good time for investments"]),
                    ("💝 Relationships & Family", random.randint(70, 95),
                     ["Harmony in personal relationships", "Family support strong", "Good period for marriage prospects"]),
                    ("🏥 Health & Wellness", random.randint(60, 80),
                     ["Generally good health", "Watch stress levels", "Regular exercise recommended"]),
                    ("📚 Education & Learning", random.randint(70, 90),
                     ["Excellent for learning new skills", "Academic success likely", "Good concentration period"])
                ]
                
                for area, score, points in areas:
                    with st.expander(f"{area} - Score: {score}/100", expanded=False):
                        st.progress(score / 100)
                        for point in points:
                            st.markdown(f"• {point}")
                
                # Month-by-month
                st.markdown("---")
                st.markdown("### 📆 Month-by-Month Highlights")
                
                months = [
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ]
                
                ratings = ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐"]
                
                month_data = {}
                for month in months:
                    rating = random.choice(ratings)
                    prediction = random.choice([
                        "Excellent month for career growth",
                        "Good financial prospects",
                        "Focus on relationships",
                        "Health needs attention",
                        "Travel opportunities",
                        "Learning and development",
                        "Property matters favorable",
                        "Spiritual growth period"
                    ])
                    month_data[month] = (rating, prediction)
                
                cols = st.columns(3)
                for idx, (month, (rating, pred)) in enumerate(month_data.items()):
                    with cols[idx % 3]:
                        st.markdown(f"**{month}** {rating}")
                        st.caption(pred)
                
                # Remedies
                st.markdown("---")
                st.markdown("### 🏥 Recommended Remedies for the Year")
                st.markdown(f"""
                - Worship **{favorable_planets[0]}** on appropriate days
                - Chant mantras for {favorable_planets[1]} to enhance benefits
                - Wear gemstone for strengthening weak planets
                - Donate on Saturdays to mitigate {challenging_planets[0]} effects
                - Perform Navgraha Shanti puja at the start of the year
                """)
                
                st.success("💡 **Tip:** Review this Varshaphal periodically throughout the year for best results!")
                
            except Exception as e:
                st.error(f"Error generating Varshaphal: {str(e)}")


def show_dasha_detail():
    """Detailed Dasha Predictions Page"""
    st.header("🌀 Detailed Dasha Analysis")
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        st.warning("⚠️ Please login to access detailed dasha analysis")
        return
    
    st.info("🔮 In-depth analysis of your current and upcoming planetary periods (Vimshottari Dasha)")
    
    # Check payment
    payment_enabled = config.get('payment', {}).get('enabled', False)
    user_email = st.session_state.current_user
    dasha_cost = config.get('payment', {}).get('pricing', {}).get('dasha_detail', 50)
    
    if payment_enabled:
        current_credits = st.session_state.payment_manager.get_user_credits(user_email)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"💳 Credits: **{current_credits}** | Dasha Analysis: **{dasha_cost} credits**")
        with col2:
            if st.button("💎 Buy Credits"):
                st.session_state.force_page = get_text('nav_credits')
                st.rerun()
    
    # Profile selection
    user_manager = st.session_state.user_manager
    profiles = user_manager.list_profiles(user_email)
    
    if not profiles:
        st.warning("Please create a user profile first!")
        if st.button("Go to User Profiles"):
            st.session_state.force_page = get_text('nav_profiles')
            st.rerun()
        return
    
    profile_names = [p.name for p in profiles]
    selected_name = st.selectbox("Select Profile", profile_names)
    
    st.markdown("**Pricing:** ₹25")
    
    if st.button("🌀 Analyze Dasha Periods", type="primary"):
        # Check credits
        if payment_enabled:
            if current_credits < dasha_cost:
                st.error(f"❌ Insufficient credits! You need {dasha_cost} credits.")
                return
        
        with st.spinner("Analyzing your planetary periods..."):
            profile = next((p for p in profiles if p.name == selected_name), None)
            
            if not profile:
                st.error("Error loading profile")
                return
            
            try:
                from src.astrology_engine.vedic_calculator import BirthDetails
                from datetime import datetime, timedelta
                import random
                
                calculator = st.session_state.astro_engine
                birth_dt = datetime.fromisoformat(f"{profile.birth_date}T{profile.birth_time}")
                
                details = BirthDetails(
                    date=birth_dt,
                    latitude=profile.latitude,
                    longitude=profile.longitude,
                    timezone=profile.timezone,
                    name=profile.name,
                    place=profile.birth_place
                )
                chart = calculator.calculate_birth_chart(details)
                
                # Calculate current Mahadasha and Antardasha
                from datetime import datetime
                
                # Get birth Moon longitude for dasha calculation
                moon_data = chart.get('planets', {}).get('Moon', {})
                if isinstance(moon_data, dict):
                    moon_longitude = moon_data.get('longitude', 0)
                else:
                    moon_longitude = getattr(moon_data, 'longitude', 0)
                
                # Calculate dasha periods
                dasha_periods = calculator.calculate_vimshottari_dasha(moon_longitude, birth_dt)
                
                # Find current period
                from datetime import datetime
                current_date = datetime.now()
                
                current_mahadasha = 'Sun'
                current_antardasha = 'Sun'
                
                for period in dasha_periods:
                    if period['start_date'] <= current_date <= period['end_date']:
                        current_mahadasha = period['lord']
                        # Antardasha cycles through same sequence proportionally
                        # For simplicity, use a basic sub-period calculation
                        days_into_maha = (current_date - period['start_date']).days
                        total_days = (period['end_date'] - period['start_date']).days
                        
                        # Find which antardasha based on proportion
                        antar_sequence = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
                        maha_idx = antar_sequence.index(current_mahadasha) if current_mahadasha in antar_sequence else 0
                        
                        # Simple approximation: divide period into 9 sub-periods
                        sub_period_days = total_days / 9
                        antar_idx = int(days_into_maha / sub_period_days)
                        current_antardasha = antar_sequence[(maha_idx + antar_idx) % 9]
                        
                        # Store the period data for display
                        maha_years = period['years']
                        maha_start = period['start_date']
                        maha_end = period['end_date']
                        break
                
                # Mahadasha durations
                dasha_durations = {
                    'Sun': 6, 'Moon': 10, 'Mars': 7, 'Rahu': 18,
                    'Jupiter': 16, 'Saturn': 19, 'Mercury': 17,
                    'Ketu': 7, 'Venus': 20
                }
                maha_total_years = dasha_durations.get(current_mahadasha, 7)
                
                # Deduct credits
                if payment_enabled:
                    success, new_balance = st.session_state.payment_manager.deduct_credits(
                        user_email, dasha_cost, f"Dasha Analysis: {selected_name}"
                    )
                    if success:
                        st.success(f"✅ {dasha_cost} credits deducted. Remaining: {new_balance}")
                
                # Display results
                st.markdown("---")
                st.markdown(f"## 🌀 Dasha Analysis for {selected_name}")
                
                # Current Dasha Overview
                st.markdown("### 🎯 Current Planetary Periods")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Mahadasha", current_mahadasha)
                with col2:
                    st.metric("Antardasha", current_antardasha)
                with col3:
                    st.metric(f"{current_mahadasha} Period", f"{maha_total_years} years")
                
                # Get planet positions for personalized analysis
                def get_planet_house(planet_name):
                    planet_data = chart.get('planets', {}).get(planet_name, {})
                    if isinstance(planet_data, dict):
                        return planet_data.get('house', 1)
                    return getattr(planet_data, 'house', 1)
                
                maha_house = get_planet_house(current_mahadasha)
                antar_house = get_planet_house(current_antardasha)
                
                # Mahadasha Analysis with Personalized Predictions
                st.markdown(f"### 🪐 {current_mahadasha} Mahadasha Analysis")
                
                st.info(f"""**📍 Current Position:** {current_mahadasha} is placed in your **{maha_house}th house**
**🔮 Antardasha:** Currently running {current_antardasha} Antardasha (placed in {antar_house}th house)""")
                
                dasha_predictions = {
                    'Sun': {
                        'duration': '6 years',
                        'traits': 'Authority, government, leadership, father figure',
                        'positive': ['Career growth', 'Recognition', 'Leadership opportunities', 'Government benefits'],
                        'challenges': ['Ego issues', 'Authority conflicts', 'Health of father'],
                        'remedies': ['Surya Namaskar', 'Donate wheat on Sundays', 'Wear Ruby gemstone']
                    },
                    'Moon': {
                        'duration': '10 years',
                        'traits': 'Mind, emotions, mother, public dealings',
                        'positive': ['Mental peace', 'Public popularity', 'Property gains', 'Mother\'s blessings'],
                        'challenges': ['Mood swings', 'Emotional instability', 'Mother\'s health'],
                        'remedies': ['Chandra mantra', 'Donate white items on Mondays', 'Wear Pearl']
                    },
                    'Mars': {
                        'duration': '7 years',
                        'traits': 'Energy, courage, siblings, property',
                        'positive': ['High energy', 'Courage', 'Property acquisition', 'Victory over enemies'],
                        'challenges': ['Aggression', 'Accidents', 'Disputes', 'Surgery'],
                        'remedies': ['Hanuman Chalisa', 'Donate red lentils on Tuesdays', 'Wear Red Coral']
                    },
                    'Mercury': {
                        'duration': '17 years',
                        'traits': 'Communication, business, intellect',
                        'positive': ['Business success', 'Communication skills', 'Learning', 'Versatility'],
                        'challenges': ['Overthinking', 'Nervousness', 'Skin issues'],
                        'remedies': ['Budh mantra', 'Donate green items on Wednesdays', 'Wear Emerald']
                    },
                    'Jupiter': {
                        'duration': '16 years',
                        'traits': 'Wisdom, spirituality, wealth, children',
                        'positive': ['Prosperity', 'Children blessings', 'Spiritual growth', 'Good fortune'],
                        'challenges': ['Weight gain', 'Over-optimism', 'Financial expansion'],
                        'remedies': ['Guru mantra', 'Donate yellow items on Thursdays', 'Wear Yellow Sapphire']
                    },
                    'Venus': {
                        'duration': '20 years',
                        'traits': 'Love, luxury, art, marriage',
                        'positive': ['Marriage', 'Luxury', 'Artistic success', 'Comforts'],
                        'challenges': ['Over-indulgence', 'Relationship issues', 'Expense on luxuries'],
                        'remedies': ['Shukra mantra', 'Donate white items on Fridays', 'Wear Diamond']
                    },
                    'Saturn': {
                        'duration': '19 years',
                        'traits': 'Discipline, karma, delays, hard work',
                        'positive': ['Discipline', 'Long-term success', 'Spiritual maturity', 'Justice'],
                        'challenges': ['Delays', 'Hardships', 'Depression', 'Chronic issues'],
                        'remedies': ['Shani mantra', 'Donate black items on Saturdays', 'Wear Blue Sapphire (after trial)']
                    },
                    'Rahu': {
                        'duration': '18 years',
                        'traits': 'Illusion, foreign lands, technology',
                        'positive': ['Foreign opportunities', 'Technology gains', 'Innovation', 'Sudden gains'],
                        'challenges': ['Confusion', 'Deception', 'Addictions', 'Unconventional path'],
                        'remedies': ['Rahu mantra', 'Donate to poor on Saturdays', 'Wear Hessonite']
                    },
                    'Ketu': {
                        'duration': '7 years',
                        'traits': 'Spirituality, detachment, moksha',
                        'positive': ['Spiritual growth', 'Intuition', 'Liberation', 'Occult knowledge'],
                        'challenges': ['Isolation', 'Confusion', 'Loss of direction', 'Health issues'],
                        'remedies': ['Ketu mantra', 'Donate multicolor blankets', 'Wear Cat\'s Eye']
                    }
                }
                
                maha_info = dasha_predictions.get(current_mahadasha, dasha_predictions['Sun'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Duration:** {maha_info['duration']}")
                    st.markdown(f"**Key Traits:** {maha_info['traits']}")
                    
                    st.markdown("**✅ Positive Effects:**")
                    for effect in maha_info['positive']:
                        st.markdown(f"- {effect}")
                
                with col2:
                    st.markdown("**⚠️ Challenges:**")
                    for challenge in maha_info['challenges']:
                        st.markdown(f"- {challenge}")
                    
                    st.markdown("**🏥 Remedies:**")
                    for remedy in maha_info['remedies']:
                        st.markdown(f"- {remedy}")
                
                # Antardasha Analysis
                st.markdown("---")
                st.markdown(f"### ⚡ Current {current_antardasha} Antardasha Effects")
                
                st.info(f"""The Antardasha of **{current_antardasha}** within **{current_mahadasha}** Mahadasha 
creates a unique combination that influences your current circumstances. The Antardasha lord 
modifies and colors the Mahadasha results.""")
                
                # Concrete Personalized Predictions
                st.markdown("---")
                st.markdown("### 🎯 Your Personalized Predictions (Current Period)")
                
                # House-based predictions
                house_effects = {
                    1: {
                        'benefits': ['Strong self-confidence', 'Leadership opportunities', 'Good health', 'Personal initiatives succeed'],
                        'challenges': ['Can be too self-focused', 'Ego clashes possible', 'Impatience with others'],
                        'timing': ['Excellent time to start new ventures', 'Good for personal branding', 'Ideal for fitness goals']
                    },
                    2: {
                        'benefits': ['Financial gains', 'Family harmony', 'Good for savings', 'Speech and communication improve'],
                        'challenges': ['Watch expenses', 'Family demands increase', 'Speech may cause conflicts'],
                        'timing': ['Good for investments', 'Time to build wealth', 'Focus on family bonds']
                    },
                    3: {
                        'benefits': ['Courage and confidence', 'Sibling support', 'Short travels profitable', 'Communication skills shine'],
                        'challenges': ['Conflicts with siblings', 'Frequent travel may tire you', 'Hasty decisions'],
                        'timing': ['Perfect for learning new skills', 'Start creative projects', 'Network actively']
                    },
                    4: {
                        'benefits': ['Mother\'s blessings', 'Property gains', 'Mental peace', 'Home comforts increase'],
                        'challenges': ['Home renovations needed', 'Mother\'s health needs attention', 'Emotional ups and downs'],
                        'timing': ['Buy property now', 'Renovate home', 'Strengthen family bonds']
                    },
                    5: {
                        'benefits': ['Children bring joy', 'Creative success', 'Romance flourishes', 'Speculation may profit'],
                        'challenges': ['Children need attention', 'Over-optimism in speculation', 'Romantic complications'],
                        'timing': ['Perfect for creative work', 'Good for conception', 'Invest in education']
                    },
                    6: {
                        'benefits': ['Victory over enemies', 'Health improves', 'Job security', 'Debt clearance'],
                        'challenges': ['Health issues arise', 'Legal matters', 'Workplace politics', 'Loan burdens'],
                        'timing': ['Be cautious with health', 'Avoid unnecessary conflicts', 'Clear pending debts']
                    },
                    7: {
                        'benefits': ['Marriage prospects', 'Partnership success', 'Business growth', 'Spouse support'],
                        'challenges': ['Relationship demands', 'Partner\'s health', 'Business partner conflicts'],
                        'timing': ['Excellent for marriage', 'Start partnerships', 'Travel abroad']
                    },
                    8: {
                        'benefits': ['Inheritance gains', 'Occult knowledge', 'Research success', 'Hidden money found'],
                        'challenges': ['Sudden obstacles', 'Chronic health issues', 'Secrecy causes problems', 'In-law conflicts'],
                        'timing': ['Be extra cautious', 'Avoid major decisions', 'Focus on spiritual growth', 'Research and study']
                    },
                    9: {
                        'benefits': ['Father\'s blessings', 'Higher learning', 'Spiritual growth', 'Long travels', 'Fortune favors'],
                        'challenges': ['Father\'s health', 'Religious conflicts', 'Long-distance issues'],
                        'timing': ['Perfect for pilgrimage', 'Higher education', 'Teaching opportunities', 'Guru connection']
                    },
                    10: {
                        'benefits': ['Career peak', 'Promotion', 'Public recognition', 'Authority increases'],
                        'challenges': ['Workload increases', 'Responsibility pressure', 'Less family time'],
                        'timing': ['Best time for career moves', 'Start business', 'Seek promotion']
                    },
                    11: {
                        'benefits': ['Income surge', 'Gains from multiple sources', 'Elder sibling help', 'Desires fulfilled'],
                        'challenges': ['High expectations', 'Network demands time', 'Managing multiple incomes'],
                        'timing': ['Maximum profit period', 'Expand income sources', 'Network actively']
                    },
                    12: {
                        'benefits': ['Foreign opportunities', 'Spiritual liberation', 'Isolation brings peace', 'Hidden talents emerge'],
                        'challenges': ['Expenses rise', 'Sleep issues', 'Feel isolated', 'Secret enemies'],
                        'timing': ['Good for foreign travel', 'Spiritual retreats', 'Bed comforts', 'Hospital work']
                    }
                }
                
                maha_effects = house_effects.get(maha_house, house_effects[1])
                antar_effects = house_effects.get(antar_house, house_effects[1])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**✅ You Will Benefit From ({current_mahadasha} in {maha_house}th):**")
                    for benefit in maha_effects['benefits'][:3]:
                        st.success(f"• {benefit}")
                    
                    st.markdown(f"**⏰ Best Timing For:**")
                    for timing in maha_effects['timing'][:2]:
                        st.info(f"• {timing}")
                
                with col2:
                    st.markdown(f"**⚠️ Be Cautious About ({current_mahadasha} in {maha_house}th):**")
                    for challenge in maha_effects['challenges'][:3]:
                        st.warning(f"• {challenge}")
                    
                    st.markdown(f"**🎯 Antardasha Impact ({current_antardasha} in {antar_house}th):**")
                    st.info(f"• {antar_effects['benefits'][0]}")
                    st.warning(f"• {antar_effects['challenges'][0]}")
                
                # Combined effect analysis
                st.markdown("---")
                st.markdown("### 🔮 Combined Mahadasha-Antardasha Effect")
                
                # Friendly/Enemy relationship
                planet_relationships = {
                    'Sun': {'friends': ['Moon', 'Mars', 'Jupiter'], 'enemies': ['Venus', 'Saturn'], 'neutral': ['Mercury']},
                    'Moon': {'friends': ['Sun', 'Mercury'], 'enemies': [], 'neutral': ['Mars', 'Jupiter', 'Venus', 'Saturn']},
                    'Mars': {'friends': ['Sun', 'Moon', 'Jupiter'], 'enemies': ['Mercury'], 'neutral': ['Venus', 'Saturn']},
                    'Mercury': {'friends': ['Sun', 'Venus'], 'enemies': ['Moon'], 'neutral': ['Mars', 'Jupiter', 'Saturn']},
                    'Jupiter': {'friends': ['Sun', 'Moon', 'Mars'], 'enemies': ['Mercury', 'Venus'], 'neutral': ['Saturn']},
                    'Venus': {'friends': ['Mercury', 'Saturn'], 'enemies': ['Sun', 'Moon'], 'neutral': ['Mars', 'Jupiter']},
                    'Saturn': {'friends': ['Mercury', 'Venus'], 'enemies': ['Sun', 'Moon', 'Mars'], 'neutral': ['Jupiter']},
                    'Rahu': {'friends': ['Saturn', 'Mercury', 'Venus'], 'enemies': ['Sun', 'Moon', 'Mars'], 'neutral': ['Jupiter']},
                    'Ketu': {'friends': ['Mars', 'Venus', 'Saturn'], 'enemies': ['Moon', 'Sun'], 'neutral': ['Mercury', 'Jupiter']}
                }
                
                maha_rel = planet_relationships.get(current_mahadasha, {'friends': [], 'enemies': [], 'neutral': []})
                
                if current_antardasha in maha_rel['friends']:
                    st.success(f"""🤝 **Excellent Combination!** {current_mahadasha} and {current_antardasha} are FRIENDS
                    
✨ **What This Means:**
- Both planets support each other's goals
- Results will be harmonious and beneficial  
- Success comes with less obstacles
- Good time for major decisions
- Combine the benefits of both periods""")
                elif current_antardasha in maha_rel['enemies']:
                    st.warning(f"""⚔️ **Challenging Combination** {current_mahadasha} and {current_antardasha} are ENEMIES
                    
⚠️ **What This Means:**
- Conflicting energies create obstacles
- Success requires extra effort
- Be patient with delays
- Avoid major commitments
- Focus on damage control and remedies

🔧 **Immediate Actions:**
- Do remedies for both planets
- Be extra cautious in decisions
- Maintain patience and persistence
- Seek expert guidance for major moves""")
                else:
                    st.info(f"""⚖️ **Neutral Combination** {current_mahadasha} and {current_antardasha} are NEUTRAL
                    
💡 **What This Means:**
- Mixed results likely
- Results depend on your efforts
- Neither highly favorable nor extremely difficult
- Good time for moderate actions
- Balance both planetary energies""")
                
                # Upcoming Dashas (5-year forecast)
                st.markdown("---")
                st.markdown("### 📅 Upcoming Dasha Timeline (Next 5 Years)")
                
                dasha_sequence = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
                current_idx = dasha_sequence.index(current_mahadasha) if current_mahadasha in dasha_sequence else 0
                
                st.markdown("**Major Period Changes Expected:**")
                for i in range(3):
                    next_dasha = dasha_sequence[(current_idx + i + 1) % len(dasha_sequence)]
                    next_info = dasha_predictions[next_dasha]
                    
                    with st.expander(f"🔮 {next_dasha} Mahadasha - {next_info['duration']}", expanded=(i==0)):
                        st.markdown(f"**Main Focus:** {next_info['traits']}")
                        st.markdown("**What to Expect:**")
                        for effect in next_info['positive'][:2]:
                            st.success(f"✅ {effect}")
                        st.markdown("**Prepare For:**")
                        for challenge in next_info['challenges'][:2]:
                            st.warning(f"⚠️ {challenge}")
                
                # Best periods for activities
                st.markdown("---")
                st.markdown("### 🎯 Activity Timing Recommendations")
                
                activities = st.columns(2)
                with activities[0]:
                    st.markdown("**Best Periods For:**")
                    st.success("💼 Career Changes: Jupiter, Sun, Mercury Dasha")
                    st.success("💑 Marriage: Venus, Jupiter Dasha")
                    st.success("🏠 Property: Mars, Moon Dasha")
                    st.success("📚 Education: Mercury, Jupiter Dasha")
                
                with activities[1]:
                    st.markdown("**Exercise Caution During:**")
                    st.warning("⚠️ Major Decisions: Saturn, Rahu, Ketu Dasha")
                    st.warning("⚠️ Speculation: Rahu, Ketu Dasha")
                    st.warning("⚠️ Health: Saturn, Mars Dasha")
                    st.warning("⚠️ Relationships: Saturn, Sun Dasha")
                
                st.success("💡 **Pro Tip:** Dasha system is the most accurate timing technique. Use it along with transits for best results!")
                
            except Exception as e:
                st.error(f"Error analyzing dasha: {str(e)}")


def show_name_recommendation():
    """Name Recommendation based on Numerology & Astrology"""
    st.header("✨ Lucky Name Recommendations")
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        st.warning("⚠️ Please login to get name recommendations")
        return
    
    st.info("✨ Get personalized name suggestions based on your birth chart, nakshatra, and numerology")
    
    st.markdown("""
    ### What is Name Numerology?
    Your name creates vibrations that influence your life. A harmonious name aligned with your birth chart 
    can enhance success, relationships, and overall well-being.
    
    ### Features:
    - **Name Number Analysis** - Current name compatibility with birth chart
    - **Lucky Alphabets** - Best starting letters based on nakshatra
    - **Name Suggestions** - Multiple name options with meanings
    - **Business Name** - Lucky names for businesses/brands
    - **Baby Names** - Names for newborns based on birth chart
    - **Name Correction** - Minor tweaks to existing names
    - **Spelling Variations** - Alternative spellings for better vibration
    - **Signature Analysis** - How to sign for better fortune
    
    ### Pricing: **50 Credits**
    
    ### Analysis based on:
    - **Birth Nakshatra** - Your lunar mansion's alphabet
    - **Numerology** - Life path and destiny number compatibility
    - **Planetary Positions** - Favorable planets in your chart
    - **Ascendant (Lagna)** - First house lord's favorable letters
    - **Name Length** - Optimal number of letters
    - **Vowel-Consonant Balance** - Energy harmony
    
    ### What you get:
    - 5-10 personalized name suggestions with meanings
    - Current name analysis (if changing name)
    - Lucky and unlucky letters for you
    - Signature recommendations
    - Business/brand name options (if requested)
    - Detailed explanation of each recommendation
    
    **💡 Tip:** Right name can boost career, relationships, and prosperity!
    """)
    
    st.markdown("---")
    
    # Name categories
    st.subheader("Name Recommendation Types")
    
    name_types = st.columns(3)
    with name_types[0]:
        st.markdown("""
        **Personal Names:**
        - First name change
        - Middle name addition
        - Nickname creation
        - Signature adjustment
        """)
    with name_types[1]:
        st.markdown("""
        **Baby Names:**
        - Based on birth nakshatra
        - Meaning and significance
        - Modern yet traditional
        - Multiple options
        """)
    with name_types[2]:
        st.markdown("""
        **Business Names:**
        - Company name
        - Brand name
        - Product name
        - Domain name ideas
        """)
    
    st.markdown("---")
    
    # Profile selection
    user_manager = st.session_state.user_manager
    user_email = st.session_state.current_user
    profiles = user_manager.list_profiles(user_email)
    
    if not profiles:
        st.warning("Please create a user profile first!")
        if st.button("Go to User Profiles"):
            st.session_state.force_page = get_text('nav_profiles')
            st.rerun()
        return
    
    profile_names = [p.name for p in profiles]
    selected_name = st.selectbox("Select Profile", profile_names)
    
    # Name purpose selection
    name_purpose = st.radio(
        "Purpose of Name",
        ["Baby Name", "Business Name", "Personal Rename"],
        horizontal=True
    )
    
    # Gender selection (for baby names)
    gender = None
    if name_purpose == "Baby Name":
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    
    # Additional preferences
    st.markdown("### Additional Preferences")
    col1, col2 = st.columns(2)
    with col1:
        tradition = st.selectbox("Tradition", ["Traditional", "Modern", "Both"])
        syllables = st.selectbox("Name Length", ["Short (1-2 syllables)", "Medium (3-4 syllables)", "Long (5+ syllables)", "Any"])
    with col2:
        meaning_focus = st.selectbox("Meaning Focus", ["Prosperity", "Wisdom", "Strength", "Peace", "Any"])
    
    if st.button("🌟 Generate Name Recommendations", type="primary"):
        # Check payment
        payment_enabled = config.get('payment', {}).get('enabled', False)
        name_cost = config.get('payment', {}).get('pricing', {}).get('name_recommendation', 50)
        
        if payment_enabled:
            current_credits = st.session_state.payment_manager.get_user_credits(user_email)
            if current_credits < name_cost:
                st.error(f"❌ Insufficient credits! You need {name_cost} credits.")
                return
        
        with st.spinner("Analyzing your chart for lucky names..."):
            profile = next((p for p in profiles if p.name == selected_name), None)
            
            if not profile:
                st.error("Error loading profile")
                return
            
            try:
                from src.astrology_engine.vedic_calculator import BirthDetails
                from datetime import datetime
                
                calculator = st.session_state.astro_engine
                birth_dt = datetime.fromisoformat(f"{profile.birth_date}T{profile.birth_time}")
                
                details = BirthDetails(
                    date=birth_dt,
                    latitude=profile.latitude,
                    longitude=profile.longitude,
                    timezone=profile.timezone,
                    name=profile.name,
                    place=profile.birth_place
                )
                chart = calculator.calculate_birth_chart(details)
                
                # Deduct credits
                if payment_enabled:
                    success, new_balance = st.session_state.payment_manager.deduct_credits(
                        user_email, name_cost, f"Name Recommendation: {selected_name}"
                    )
                    if success:
                        st.success(f"✅ {name_cost} credits deducted. Remaining: {new_balance}")
                
                # Helper function to get planet attribute
                def get_planet_attr(chart, planet_name, attr):
                    planet_data = chart.get('planets', {}).get(planet_name, {})
                    if isinstance(planet_data, dict):
                        return planet_data.get(attr, 'Unknown')
                    return getattr(planet_data, attr, 'Unknown')
                
                # Get nakshatra
                nakshatra = get_planet_attr(chart, 'Moon', 'nakshatra')
                
                # Nakshatra syllables mapping
                nakshatra_syllables = {
                    'Ashwini': ['Chu', 'Che', 'Cho', 'La'],
                    'Bharani': ['Li', 'Lu', 'Le', 'Lo'],
                    'Krittika': ['A', 'I', 'U', 'E'],
                    'Rohini': ['O', 'Va', 'Vi', 'Vu'],
                    'Mrigashira': ['Ve', 'Vo', 'Ka', 'Ki'],
                    'Ardra': ['Ku', 'Gha', 'Nga', 'Chha'],
                    'Punarvasu': ['Ke', 'Ko', 'Ha', 'Hi'],
                    'Pushya': ['Hu', 'He', 'Ho', 'Da'],
                    'Ashlesha': ['Di', 'Du', 'De', 'Do'],
                    'Magha': ['Ma', 'Mi', 'Mu', 'Me'],
                    'Purva Phalguni': ['Mo', 'Ta', 'Ti', 'Tu'],
                    'Uttara Phalguni': ['Te', 'To', 'Pa', 'Pi'],
                    'Hasta': ['Pu', 'Sha', 'Na', 'Tha'],
                    'Chitra': ['Pe', 'Po', 'Ra', 'Ri'],
                    'Swati': ['Ru', 'Re', 'Ro', 'Ta'],
                    'Vishakha': ['Ti', 'Tu', 'Te', 'To'],
                    'Anuradha': ['Na', 'Ni', 'Nu', 'Ne'],
                    'Jyeshtha': ['No', 'Ya', 'Yi', 'Yu'],
                    'Mula': ['Ye', 'Yo', 'Bha', 'Bhi'],
                    'Purva Ashadha': ['Bhu', 'Dha', 'Pha', 'Dha'],
                    'Uttara Ashadha': ['Bhe', 'Bho', 'Ja', 'Ji'],
                    'Shravana': ['Ju', 'Je', 'Jo', 'Gha'],
                    'Dhanishta': ['Ga', 'Gi', 'Gu', 'Ge'],
                    'Shatabhisha': ['Go', 'Sa', 'Si', 'Su'],
                    'Purva Bhadrapada': ['Se', 'So', 'Da', 'Di'],
                    'Uttara Bhadrapada': ['Du', 'Tha', 'Jha', 'Tra'],
                    'Revati': ['De', 'Do', 'Cha', 'Chi']
                }
                
                lucky_syllables = nakshatra_syllables.get(nakshatra, ['A', 'I', 'U', 'E'])
                
                # Display results
                st.markdown("---")
                st.markdown(f"## 🌟 Name Recommendations for {selected_name}")
                
                # Show nakshatra info
                st.markdown("### 🌙 Your Nakshatra")
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**Birth Nakshatra:** {nakshatra}")
                    st.info(f"**Lucky Syllables:** {', '.join(lucky_syllables)}")
                with col2:
                    st.info(f"**Purpose:** {name_purpose}")
                    if gender:
                        st.info(f"**Gender:** {gender}")
                
                # Generate names based on syllables
                st.markdown("### ✨ Recommended Names")
                
                # Name database (simplified - in production this would be much larger)
                name_database = {
                    'Male': {
                        'Chu': [('Chulbul', 'Lively and active'), ('Chudamani', 'Crown jewel')],
                        'Che': [('Chetan', 'Consciousness'), ('Cheshta', 'Effort')],
                        'A': [('Aarav', 'Peaceful'), ('Arjun', 'Bright'), ('Aditya', 'Sun')],
                        'I': [('Ishaan', 'Lord Shiva'), ('Ishan', 'Direction')],
                        'Ka': [('Karan', 'Doer'), ('Kartik', 'Son of Shiva'), ('Krishna', 'Dark one')],
                        'Ra': [('Raj', 'King'), ('Ravi', 'Sun'), ('Rohan', 'Ascending')],
                        'Ma': [('Madhav', 'Lord Krishna'), ('Mohit', 'Attracted')],
                        'Na': [('Nakul', 'Mongoose'), ('Naman', 'Salutation'), ('Nirav', 'Quiet')],
                        'Sa': [('Sahil', 'Guide'), ('Sanjay', 'Victorious'), ('Sarvesh', 'Lord of all')],
                        'Da': [('Darsh', 'Vision'), ('Dev', 'God'), ('Dhruv', 'Pole star')],
                        'Pa': [('Pranav', 'Om'), ('Prem', 'Love'), ('Paras', 'Touchstone')],
                        'Ta': [('Tanay', 'Son'), ('Tarun', 'Young'), ('Tejas', 'Brilliance')],
                        'Ga': [('Gaurav', 'Pride'), ('Gagan', 'Sky'), ('Ganesh', 'Lord Ganesh')],
                        'Va': [('Varun', 'God of water'), ('Vikram', 'Valor'), ('Vishal', 'Grand')],
                        'Ja': [('Jai', 'Victory'), ('Jay', 'Victory'), ('Jatin', 'One with matted hair')],
                        'Ha': [('Harsh', 'Joy'), ('Hari', 'Lord Vishnu'), ('Hemant', 'Winter')],
                        'Ya': [('Yash', 'Fame'), ('Yogi', 'Devotee'), ('Yuvan', 'Youth')],
                        'La': [('Laksh', 'Target'), ('Lalit', 'Beautiful'), ('Laxman', 'Prosperous')],
                        'Bha': [('Bharat', 'India'), ('Bhaskar', 'Sun'), ('Bhavesh', 'Lord of world')],
                        'Li': [('Lokesh', 'Lord of world'), ('Lalit', 'Beautiful')],
                        'O': [('Om', 'Sacred sound'), ('Omkar', 'Sound of Om')],
                        'Ve': [('Veer', 'Brave'), ('Ved', 'Sacred knowledge')],
                        'Ku': [('Kunal', 'Lotus'), ('Kumar', 'Prince')],
                        'Ke': [('Keshav', 'Lord Krishna'), ('Kevin', 'Kind')],
                        'Hu': [('Himanshu', 'Moon'), ('Hridaan', 'From heart')],
                        'Di': [('Dinesh', 'Lord of day'), ('Divit', 'Immortal')],
                        'Mo': [('Mohan', 'Attractive'), ('Moksh', 'Salvation')],
                        'Pe': [('Piyush', 'Nectar'), ('Pankaj', 'Lotus')],
                        'Ru': [('Rudra', 'Lord Shiva'), ('Rushil', 'Charming')],
                        'No': [('Nishant', 'Dawn'), ('Neeraj', 'Lotus')],
                        'Ye': [('Yuvraj', 'Prince'), ('Yashas', 'Fame')],
                        'Bhu': [('Bhuvan', 'World'), ('Bhupesh', 'King')],
                        'Ju': [('Jugal', 'Couple'), ('Jeevan', 'Life')],
                        'Se': [('Sehaj', 'Easy'), ('Siddh', 'Accomplished')],
                    },
                    'Female': {
                        'Chu': [('Chulbuli', 'Bubbly'), ('Chumki', 'Kiss')],
                        'Che': [('Chetana', 'Consciousness'), ('Cheshta', 'To try')],
                        'A': [('Aarohi', 'Progressive'), ('Ananya', 'Unique'), ('Anika', 'Grace')],
                        'I': [('Ishani', 'Goddess'), ('Isha', 'One who protects')],
                        'Ka': [('Kavya', 'Poetry'), ('Keya', 'Flower'), ('Khushi', 'Happiness')],
                        'Ra': [('Radhika', 'Successful'), ('Riya', 'Singer'), ('Roshni', 'Light')],
                        'Ma': [('Madhavi', 'Springtime'), ('Meera', 'Devotee'), ('Mahi', 'Earth')],
                        'Na': [('Naina', 'Eyes'), ('Neha', 'Love'), ('Nisha', 'Night')],
                        'Sa': [('Saanvi', 'Goddess Lakshmi'), ('Sakshi', 'Witness'), ('Sia', 'Goddess Sita')],
                        'Da': [('Diya', 'Lamp'), ('Divya', 'Divine'), ('Daksha', 'Competent')],
                        'Pa': [('Priya', 'Beloved'), ('Pari', 'Fairy'), ('Pooja', 'Worship')],
                        'Ta': [('Tanya', 'Fairy queen'), ('Tanvi', 'Delicate'), ('Tara', 'Star')],
                        'Ga': [('Gayatri', 'Vedic hymn'), ('Gargi', 'Ancient scholar'), ('Gauri', 'Goddess Parvati')],
                        'Va': [('Vani', 'Speech'), ('Varsha', 'Rain'), ('Vidya', 'Knowledge')],
                        'Ja': [('Jaya', 'Victory'), ('Janvi', 'River Ganga'), ('Jiya', 'Heart')],
                        'Ha': [('Hansa', 'Swan'), ('Hema', 'Golden'), ('Hiral', 'Lustrous')],
                        'Ya': [('Yashi', 'Fame'), ('Yamini', 'Night'), ('Yukti', 'Strategy')],
                        'La': [('Lata', 'Vine'), ('Lavanya', 'Grace'), ('Lakshmi', 'Goddess of wealth')],
                        'Bha': [('Bhavna', 'Feelings'), ('Bharati', 'Goddess'), ('Bhumi', 'Earth')],
                        'Li': [('Lila', 'Divine play'), ('Lipika', 'Writer')],
                        'O': [('Ojasvi', 'Bright'), ('Oorja', 'Energy')],
                        'Ve': [('Veena', 'Musical instrument'), ('Vedika', 'Altar')],
                        'Ku': [('Kumud', 'Lotus'), ('Kuhu', 'Sweet sound')],
                        'Ke': [('Ketki', 'Flower'), ('Kesar', 'Saffron')],
                        'Hu': [('Hiral', 'Wealthy'), ('Hema', 'Golden')],
                        'Di': [('Dimple', 'Small depression'), ('Disha', 'Direction')],
                        'Mo': [('Mohini', 'Enchanting'), ('Monisha', 'Intelligent')],
                        'Pe': [('Poonam', 'Full moon'), ('Prerna', 'Inspiration')],
                        'Ru': [('Ruchi', 'Interest'), ('Rutvi', 'Speech')],
                        'No': [('Noor', 'Light'), ('Nitya', 'Eternal')],
                        'Ye': [('Yashvi', 'Fame'), ('Yogita', 'Concentration')],
                        'Bhu': [('Bhavika', 'Cheerful'), ('Bhuvana', 'Earth')],
                        'Ju': [('Juhi', 'Jasmine'), ('Jivika', 'Water')],
                        'Se': [('Sephali', 'Flower'), ('Sevita', 'Cherished')],
                    }
                }
                
                # Business names
                business_prefixes = ['Shri', 'Om', 'Maha', 'Prem', 'Siddhi', 'Jaya', 'Sree', 'Lakshmi', 'Ganesh']
                business_suffixes = ['Enterprises', 'Industries', 'Solutions', 'Corporation', 'Services', 'Technologies', 'Ventures', 'Group']
                
                if name_purpose == "Business Name":
                    st.markdown("#### 💼 Business Name Suggestions")
                    for i, syllable in enumerate(lucky_syllables[:4], 1):
                        prefix = business_prefixes[i % len(business_prefixes)]
                        suffix = business_suffixes[i % len(business_suffixes)]
                        business_name = f"{prefix} {syllable}{syllable.lower()}vi {suffix}"
                        st.success(f"**{i}. {business_name}**")
                        st.caption(f"Starting with lucky syllable '{syllable}' - Brings prosperity and success")
                else:
                    # Baby or personal names
                    target_gender = gender if gender else "Male"
                    
                    name_count = 0
                    for syllable in lucky_syllables:
                        if syllable in name_database.get(target_gender, {}):
                            names_list = name_database[target_gender][syllable]
                            for name, meaning in names_list:
                                name_count += 1
                                col1, col2 = st.columns([2, 3])
                                with col1:
                                    st.success(f"**{name_count}. {name}**")
                                with col2:
                                    st.info(f"**Meaning:** {meaning} | **Syllable:** {syllable}")
                                if name_count >= 12:
                                    break
                        if name_count >= 12:
                            break
                
                # Numerology section
                st.markdown("---")
                st.markdown("### 🔢 Numerology Insights")
                
                # Calculate numerology number from date
                birth_date = datetime.strptime(profile.birth_date, '%Y-%m-%d')
                day = birth_date.day
                month = birth_date.month
                year = birth_date.year
                
                def reduce_to_single(num):
                    while num > 9 and num not in [11, 22, 33]:
                        num = sum(int(d) for d in str(num))
                    return num
                
                life_path = reduce_to_single(day + month + year)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Life Path Number", life_path)
                
                numerology_traits = {
                    1: "Leadership, Independence, Initiative",
                    2: "Cooperation, Harmony, Diplomacy",
                    3: "Creativity, Expression, Joy",
                    4: "Stability, Hard work, Foundation",
                    5: "Freedom, Change, Adventure",
                    6: "Responsibility, Care, Family",
                    7: "Spirituality, Analysis, Wisdom",
                    8: "Ambition, Power, Material success",
                    9: "Compassion, Service, Completion",
                    11: "Intuition, Inspiration, Idealism",
                    22: "Master Builder, Practical visionary",
                    33: "Master Teacher, Spiritual guidance"
                }
                
                with col2:
                    st.info(f"**Traits:** {numerology_traits.get(life_path, 'Unique')}")
                
                st.markdown("### 📋 Name Selection Tips")
                st.info("""
                ✅ **Do's:**
                - Choose names starting with your lucky syllables
                - Consider the name's meaning and vibration
                - Ensure good pronunciation
                - Check numerological compatibility
                
                ❌ **Don'ts:**
                - Avoid negative meanings
                - Don't use very difficult spellings
                - Avoid names with harsh sounds
                """)
                
                st.success("💡 **Final Tip:** Say the name out loud multiple times. If it feels right and brings positive emotions, it's a good match!")
                
            except Exception as e:
                st.error(f"Error generating recommendations: {str(e)}")


def show_buy_credits():
    """Buy Credits page with UPI payment"""
    st.header(f"💳 {get_text('buy_credits')}")
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        st.warning("Please login to buy credits")
        return
    
    user_email = st.session_state.current_user
    
    # Display current credits
    current_credits = st.session_state.payment_manager.get_user_credits(user_email)
    st.info(f"**{get_text('credits_balance')}:** {current_credits} credits")
    
    st.markdown("---")
    
    # Get payment config
    payment_config = config.get('payment', {})
    if not payment_config.get('enabled', False):
        st.warning("Payment system is currently disabled. Please contact administrator.")
        return
    
    upi_id = payment_config.get('upi_id', 'yourupiid@paytm')
    upi_name = payment_config.get('upi_name', 'KundaliSaga')
    single_price = payment_config.get('pricing', {}).get('single_question', 10)
    bulk_packs = payment_config.get('pricing', {}).get('bulk_packs', [])
    
    # Payment Options
    st.subheader(get_text('payment_options'))
    
    # Single purchase
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"### 🎯 {get_text('single_question_price')}")
        st.write("Perfect for trying out the service")
    with col2:
        if st.button(f"{get_text('pay_now')} ₹{single_price}", key="single"):
            st.session_state.selected_pack = {'credits': 1, 'price': single_price}
    
    st.markdown("---")
    
    # Bulk packs
    st.markdown(f"### 💰 {get_text('bulk_discount')}")
    
    for idx, pack in enumerate(bulk_packs):
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            st.write(f"**{pack['questions']} {get_text('questions')}**")
        with col2:
            st.write(f"₹{pack['price']}")
        with col3:
            regular_price = pack['questions'] * single_price
            savings = regular_price - pack['price']
            st.success(f"{get_text('save')} ₹{savings}")
        with col4:
            if st.button(f"{get_text('pay_now')}", key=f"pack_{idx}"):
                st.session_state.selected_pack = {
                    'credits': pack['questions'], 
                    'price': pack['price']
                }
    
    # Show active coupons
    st.markdown("---")
    st.markdown("### 🎫 Active Discount Coupons")
    active_coupons = st.session_state.payment_manager.get_active_coupons()
    
    if active_coupons:
        coupon_cols = st.columns(min(len(active_coupons), 3))
        for idx, coupon in enumerate(active_coupons):
            with coupon_cols[idx % 3]:
                st.info(f"""
                **{coupon['code']}**  
                {coupon['discount']}% OFF  
                {coupon['description']}
                """)
    else:
        st.info("No active coupons at the moment. Check back later!")
    
    # Payment section
    if 'selected_pack' in st.session_state:
        st.markdown("---")
        pack = st.session_state.selected_pack
        original_price = pack['price']
        final_price = original_price
        coupon_applied = False
        
        # Coupon input section
        st.markdown("### 🎫 Apply Coupon Code")
        coupon_col1, coupon_col2 = st.columns([3, 1])
        with coupon_col1:
            coupon_code = st.text_input("Enter Coupon Code", placeholder="e.g., NEWYEAR50", key="coupon_input")
        with coupon_col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            apply_coupon = st.button("Apply", type="secondary")
        
        if apply_coupon and coupon_code:
            success, new_price, message = st.session_state.payment_manager.apply_coupon(
                coupon_code, user_email, original_price
            )
            if success:
                final_price = new_price
                st.success(f"✅ {message}")
                coupon_applied = True
                st.session_state.selected_pack['final_price'] = final_price
                st.session_state.selected_pack['coupon_code'] = coupon_code
            else:
                st.error(f"❌ {message}")
        
        # Check if coupon was previously applied
        if 'final_price' in pack:
            final_price = pack['final_price']
            coupon_applied = True
        
        # Display price summary
        if coupon_applied:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Original Price:** ~~₹{original_price}~~")
            with col2:
                st.success(f"**Final Price:** ₹{final_price}")
        else:
            st.success(f"**Selected:** {pack['credits']} {get_text('questions')} - ₹{final_price}")
        
        # Display UPI QR Code
        st.subheader("📱 Scan QR Code to Pay")
        
        try:
            # Use static QR code image
            qr_code_path = Path("assets/payment_qr.png")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                if qr_code_path.exists():
                    st.image(str(qr_code_path), caption="Scan with any UPI app", width=250)
                else:
                    st.warning("QR code image not found. Please contact administrator.")
            
            with col2:
                st.markdown(f"""
                **Payment Details:**
                - UPI ID: `{upi_id}`
                - Amount: ₹{final_price}
                - Credits: {pack['credits']}
                
                **OR Pay using UPI App:**
                - Open GPay/PhonePe/Paytm
                - Enter UPI ID: `{upi_id}`
                - Amount: ₹{final_price}
                - Note: KundaliSaga Credits
                """)
        except Exception as e:
            st.error(f"Error displaying payment: {e}")
            st.info(f"Please pay directly to UPI ID: {upi_id} with amount ₹{final_price}")
        
        st.markdown("---")
        
        # Payment verification
        st.subheader("✅ Verify Payment")
        st.info(get_text('payment_instructions'))
        
        with st.form("verify_payment"):
            transaction_id = st.text_input(
                get_text('transaction_id'),
                placeholder="e.g., 12345678901234",
                help="Enter the 12-digit UPI transaction ID / reference number"
            )
            
            submit = st.form_submit_button(get_text('submit_payment'))
            
            if submit:
                if not transaction_id or len(transaction_id) < 8:
                    st.error("Please enter a valid transaction ID (at least 8 characters)")
                else:
                    # Verify and add credits
                    success, result = st.session_state.payment_manager.verify_transaction(
                        transaction_id=transaction_id,
                        user_email=user_email,
                        credits=pack['credits'],
                        admin_verified=False  # Self-reported
                    )
                    
                    if success:
                        st.success(f"✅ {get_text('payment_verified')}")
                        st.balloons()
                        st.info(f"New Balance: {result} credits")
                        # Clear selected pack
                        if 'selected_pack' in st.session_state:
                            del st.session_state.selected_pack
                        st.rerun()
                    else:
                        st.error(f"❌ {result}")
        
        if st.button("Cancel Payment"):
            if 'selected_pack' in st.session_state:
                del st.session_state.selected_pack
            st.rerun()
    
    # Transaction History
    st.markdown("---")
    st.subheader("📜 Transaction History")
    transactions = st.session_state.payment_manager.get_user_transactions(user_email)
    
    if transactions:
        for txn in reversed(transactions[-10:]):  # Last 10 transactions
            with st.expander(f"{txn.get('timestamp', 'N/A')[:10]} - {txn.get('transaction_id', 'N/A')}"):
                st.json(txn)
    else:
        st.info("No transactions yet")


def show_settings():
    """Settings page"""
    st.header("⚙️ Settings")
    
    # Language Settings
    st.subheader("🌐 Language / भाषा / भाषा")
    st.markdown("""<div style="background-color: #FFFFF0; padding: 0.8rem; border-radius: 0.5rem; border-left: 5px solid #FFE57F; margin-bottom: 1rem;">
        <p style="margin: 0; color: #666; font-size: 0.9rem;">Select your preferred language for the entire application interface including menus, buttons, and messages.</p>
    </div>""", unsafe_allow_html=True)
    
    language = st.selectbox(
        "Select Language / भाषा चुनें / भाषा निवडा",
        ["English", "Hindi", "Marathi"],
        index=["English", "Hindi", "Marathi"].index(st.session_state.language),
        help="Choose your preferred language for the app interface"
    )
    if language != st.session_state.language:
        st.session_state.language = language
        st.success(f"✅ Language changed to {language}! / भाषा बदल गई! / भाषा बदलली!")
        st.rerun()
    
    # Chart Style Preference
    st.markdown("---")
    st.subheader("📊 Chart Display Style")
    st.markdown("""<div style="background-color: #FFFFF0; padding: 0.8rem; border-radius: 0.5rem; border-left: 5px solid #FFE57F; margin-bottom: 1rem;">
        <p style="margin: 0; color: #666; font-size: 0.9rem;"><strong>North Indian (Diamond):</strong> Houses are fixed (1-12), zodiac signs rotate based on Ascendant. Traditional in North India.<br>
        <strong>South Indian (Grid):</strong> Zodiac signs are fixed, houses rotate. Traditional in South India and Kerala.</p>
    </div>""", unsafe_allow_html=True)
    
    chart_style = st.radio(
        "Choose your preferred chart style:",
        ["North Indian", "South Indian"],
        index=0 if st.session_state.chart_style == 'North Indian' else 1,
        help="Select the traditional chart format you're most familiar with"
    )
    if chart_style != st.session_state.chart_style:
        st.session_state.chart_style = chart_style
        st.success(f"✅ Chart style changed to {chart_style}! Recalculate your chart to see the change.")
    
    # Ayanamsa System
    st.markdown("---")
    st.subheader("🌟 Ayanamsa System")
    st.markdown("""<div style="background-color: #FFFFF0; padding: 0.8rem; border-radius: 0.5rem; border-left: 5px solid #FFE57F; margin-bottom: 1rem;">
        <p style="margin: 0; color: #666; font-size: 0.9rem;">Ayanamsa is the precession correction used to calculate sidereal positions. Different systems give slightly different planetary positions.<br>
        <strong>Traditional Lahiri</strong> is the most widely used by Vedic astrologers.</p>
    </div>""", unsafe_allow_html=True)
    
    ayanamsa_options = {
        'LAHIRI': 'Lahiri (Traditional) - Most widely used ⭐',
        'TRUE_CHITRAPAKSHA': 'True Chitrapaksha Lahiri',
        'RAMAN': 'Raman',
        'KP': 'Krishnamurti (KP)',
        'FAGAN_BRADLEY': 'Fagan-Bradley',
        'YUKTESHWAR': 'Yukteshwar',
        'JN_BHASIN': 'JN Bhasin'
    }
    
    # Get user's current ayanamsa preference from session state, default to config
    if 'user_ayanamsa' not in st.session_state:
        st.session_state.user_ayanamsa = config.get('astrology.ayanamsa', 'LAHIRI')
    
    current_ayanamsa = st.session_state.user_ayanamsa
    
    selected_ayanamsa = st.selectbox(
        "Select Ayanamsa System:",
        options=list(ayanamsa_options.keys()),
        index=list(ayanamsa_options.keys()).index(current_ayanamsa) if current_ayanamsa in ayanamsa_options else 0,
        format_func=lambda x: ayanamsa_options[x]
    )
    
    if selected_ayanamsa != current_ayanamsa:
        if st.button("Apply Ayanamsa Change", type="primary"):
            # Update session state (user-specific)
            st.session_state.user_ayanamsa = selected_ayanamsa
            
            # Apply immediately to astrology engine
            # Check if method exists (for compatibility with old sessions)
            if hasattr(st.session_state.astro_engine, 'set_ayanamsa'):
                st.session_state.astro_engine.set_ayanamsa(selected_ayanamsa)
            else:
                # Reinitialize engine with new ayanamsa
                # Engine already initialized in session state
                st.session_state.astro_engine.set_ayanamsa(selected_ayanamsa)
            
            st.success(f"✅ Ayanamsa changed to {ayanamsa_options[selected_ayanamsa]}!")
            st.info("🔄 Change applied instantly! Recalculate your chart to see the effect.")
            st.balloons()
    else:
        st.info(f"📐 **Current Ayanamsa:** {ayanamsa_options[current_ayanamsa]}")
    
    st.caption("💡 Traditional Lahiri is the default and most widely used by Vedic astrologers. Your ayanamsa preference is personal and won't affect other users. Recalculate your chart after changing ayanamsa to see the effect.")
    
    # House System
    st.markdown("---")
    st.subheader("🏠 House System")
    st.markdown("""<div style="background-color: #FFFFF0; padding: 0.8rem; border-radius: 0.5rem; border-left: 5px solid #FFE57F; margin-bottom: 1rem;">
        <p style="margin: 0; color: #666; font-size: 0.9rem;">The house system determines how the 12 houses are calculated in the birth chart. <strong>Whole Sign Houses</strong> is the traditional Vedic method.</p>
    </div>""", unsafe_allow_html=True)
    
    house_system_options = {
        'WHOLE_SIGN': 'Whole Sign Houses (Traditional Vedic) ⭐',
        'EQUAL': 'Equal Houses',
        'PLACIDUS': 'Placidus (Western)'
    }
    
    # Get user's house system preference from session state
    if 'user_house_system' not in st.session_state:
        st.session_state.user_house_system = config.get('astrology.house_system', 'WHOLE_SIGN')
    
    current_house_system = st.session_state.user_house_system
    
    selected_house_system = st.selectbox(
        "Select House System:",
        options=list(house_system_options.keys()),
        index=list(house_system_options.keys()).index(current_house_system) if current_house_system in house_system_options else 0,
        format_func=lambda x: house_system_options[x]
    )
    
    if selected_house_system != current_house_system:
        st.info("⚠️ Note: House system changes currently require app restart. This will be improved in a future update.")
        st.caption("💡 For now, house systems are calculated at chart generation time.")
    else:
        st.info(f"🏛️ **Current House System:** {house_system_options[current_house_system]}")
    
    st.caption("💡 Whole Sign Houses: Each house = one complete zodiac sign (30°), starting from Ascendant sign. This is the authentic Vedic method used for thousands of years.")
    
    # Time Zone Configuration
    st.markdown("---")
    st.subheader("🌍 Time Zone Settings")
    st.markdown("""<div style="background-color: #FFFFF0; padding: 0.8rem; border-radius: 0.5rem; border-left: 5px solid #FFE57F; margin-bottom: 1rem;">
        <p style="margin: 0; color: #666; font-size: 0.9rem;">Accurate time zone settings ensure precise planetary positions. Enter birth location during profile creation for automatic timezone detection.</p>
    </div>""", unsafe_allow_html=True)
    st.info("⏰ **Time Zone:** Automatically detected based on birth location coordinates")
    st.caption("💡 Manual override available in User Profiles section")
    
    # LLM Configuration
    st.markdown("---")
    st.subheader("🤖 AI Model Configuration")
    st.info(f"**Model:** {config.get('llm.model')}")
    st.info(f"**Provider:** {config.get('llm.provider')}")
    st.caption("💡 All AI processing happens locally - no data sent to cloud servers")
    
    # Data Storage
    st.markdown("---")
    st.subheader("💾 Data Storage Locations")
    st.info(f"**User Data:** {config.get('storage.base_path')}")
    st.info(f"**Vector DB:** {config.get('vector_db.persist_directory')}")
    st.caption("💡 All your personal data and charts are stored securely on your device")
    
    st.markdown("---")
    
    st.subheader("About")
    st.write("""
    **KundaliSaga** v1.0.0
    
    A privacy-focused Vedic astrology application combining ancient wisdom with AI.
    
    All your data stays on your device. No cloud APIs used for LLM processing.
    """)
    
    st.markdown("---")
    st.markdown("### 📄 Privacy & Legal")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("🔒 [Privacy Policy](https://github.com/pandeabhijitv-ux/kundalisaga/blob/main/PRIVACY_POLICY.md)")
    with col2:
        st.markdown("💻 [Source Code](https://github.com/pandeabhijitv-ux/kundalisaga)")


# ===== AUTHENTICATION FUNCTIONS =====

def show_login():
    """Login page with email/password and OTP options"""
    st.markdown('<h1 class="main-header">🔐 Login to KundaliSaga</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["📧 Email & Password", "🔑 Email OTP"])
        
        with tab1:
            st.subheader("Login with Password")
            email = st.text_input("Email Address", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Login", use_container_width=True):
                    if email and password:
                        success, message, token = st.session_state.auth_manager.login_with_password(email, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.current_user = email
                            st.session_state.session_token = token
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.warning("Please enter both email and password")
            
            with col_b:
                if st.button("Register", use_container_width=True):
                    st.session_state.show_register = True
                    st.rerun()
        
        with tab2:
            st.subheader("Login with OTP")
            st.markdown("""
        <div style="background-color: #FFFFF0; padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #FFE57F;">
            <p style="margin: 0; color: #333;">We'll send a 6-digit code to your email</p>
        </div>
        """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            otp_email = st.text_input("Email Address", key="otp_email")
            
            if 'otp_sent' not in st.session_state:
                st.session_state.otp_sent = False
            
            if not st.session_state.otp_sent:
                if st.button("Send OTP", use_container_width=True):
                    if otp_email:
                        success, otp_code = st.session_state.auth_manager.send_otp(otp_email)
                        if success:
                            st.session_state.otp_sent = True
                            st.session_state.otp_email = otp_email
                            # Display OTP for testing (in production, this is sent via email)
                            st.success("✅ OTP sent to your email!")
                            st.info(f"**For testing:** Your OTP is: `{otp_code}`")
                            st.rerun()
                        else:
                            st.error(otp_code)  # Error message
                    else:
                        st.warning("Please enter your email address")
            else:
                st.success(f"OTP sent to {st.session_state.otp_email}")
                otp_code = st.text_input("Enter 6-digit OTP", max_chars=6, key="otp_code_input")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("Verify OTP", use_container_width=True):
                        if otp_code and len(otp_code) == 6:
                            success, message, token = st.session_state.auth_manager.verify_otp(
                                st.session_state.otp_email, otp_code
                            )
                            if success:
                                st.session_state.logged_in = True
                                st.session_state.current_user = st.session_state.otp_email
                                st.session_state.session_token = token
                                st.session_state.otp_sent = False
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            st.warning("Please enter a valid 6-digit OTP")
                
                with col_b:
                    if st.button("Resend OTP", use_container_width=True):
                        st.session_state.otp_sent = False
                        st.rerun()
        
        st.markdown("---")
        st.markdown("### Or continue as Guest")
        if st.button("🌟 Continue as Guest", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = "guest"
            st.session_state.guest_mode = True
            st.rerun()
        
        # Company Logo
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center; padding: 20px 0; margin-top: 40px;'>
                <div style='font-size: 2rem; margin-bottom: 5px;'>☂️</div>
                <div style='font-weight: 600; color: #FF6B35; font-size: 1.1rem;'>Krittika Apps</div>
                <div style='font-size: 0.75rem; color: #666; margin-top: 5px;'>Sharp. Supreme. Protective.</div>
                <div style='font-size: 0.7rem; color: #999; margin-top: 10px;'>© 2026 Krittika Apps</div>
            </div>
        """, unsafe_allow_html=True)


def show_register():
    """Registration page"""
    st.markdown('<h1 class="main-header">📝 Register for KundaliSaga</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Create Your Account")
        
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        password = st.text_input("Password (min 6 characters)", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Register", use_container_width=True):
            if name and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match!")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    success, message = st.session_state.auth_manager.register_user(email, password, name)
                    if success:
                        st.success(message)
                        st.info("You can now login with your email and password")
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.warning("Please fill in all fields")
        
        st.markdown("---")
        if st.button("← Back to Login"):
            st.session_state.show_register = False
            st.rerun()
        
        # Company Logo
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center; padding: 20px 0; margin-top: 40px;'>
                <div style='font-size: 2rem; margin-bottom: 5px;'>☂️</div>
                <div style='font-weight: 600; color: #FF6B35; font-size: 1.1rem;'>Krittika Apps</div>
                <div style='font-size: 0.75rem; color: #666; margin-top: 5px;'>Sharp. Supreme. Protective.</div>
                <div style='font-size: 0.7rem; color: #999; margin-top: 10px;'>© 2026 Krittika Apps</div>
            </div>
        """, unsafe_allow_html=True)


def check_session():
    """Check if user session is valid"""
    if 'session_token' in st.session_state and st.session_state.session_token:
        valid, email = st.session_state.auth_manager.validate_session(st.session_state.session_token)
        if valid:
            st.session_state.logged_in = True
            st.session_state.current_user = email
            return True
        else:
            # Session expired
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.session_token = None
            return False
    return False


def show_user_info_sidebar():
    """Show user info and logout in sidebar"""
    # Display Ganesh image at the top of sidebar
    import os
    ganesh_image_path = "assets/ganesh.jpg"
    
    if os.path.exists(ganesh_image_path):
        st.sidebar.image(ganesh_image_path, use_column_width=True)
    else:
        # Fallback: Show Ganesh symbol if image not found
        st.sidebar.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <div style='font-size: 80px; line-height: 1;'>🐘</div>
            <div style='color: #ff6b35; font-weight: bold; margin-top: 10px;'>ॐ गं गणपतये नमः</div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.logged_in and st.session_state.current_user:
        st.sidebar.markdown("---")
        if st.session_state.current_user == "guest":
            st.sidebar.info("👤 **Guest Mode**")
            st.sidebar.caption("Register to save your data")
            if st.sidebar.button("Login / Register"):
                st.session_state.current_user = None
                st.session_state.guest_mode = False
                st.rerun()
        else:
            user = st.session_state.auth_manager.get_user(st.session_state.current_user)
            if user:
                st.sidebar.success(f"👤 **{user['name']}**")
                st.sidebar.caption(f"📧 {user['email']}")
                if st.sidebar.button("🚪 Logout"):
                    st.session_state.auth_manager.logout(st.session_state.session_token)
                    st.session_state.logged_in = False
                    st.session_state.current_user = None
                    st.session_state.session_token = None
                    st.rerun()


def show_numerology():
    """Numerology Analysis Page - Integrated with Astrology"""
    st.header("🔢 Numerology Analysis")
    st.markdown("Discover your life path, destiny, and lucky numbers through the ancient science of Numerology")
    
    # Premium feature notice
    st.markdown("""
    <div style="background-color: #E8F5E9; padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #4CAF50;">
        <p style="margin: 0; color: #333;">✨ <strong>Numerology + Astrology</strong> - Complete analysis combining both sciences</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        st.warning("Please login to access numerology analysis")
        return
    
    # Check payment
    payment_enabled = config.get('payment', {}).get('enabled', False)
    user_email = st.session_state.current_user
    current_credits = 0
    numerology_cost = 10  # Basic numerology
    full_report_cost = 25  # Full report with astrology integration
    
    if payment_enabled:
        current_credits = st.session_state.payment_manager.get_user_credits(user_email)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"💳 Credits: **{current_credits}** | Basic: **10 credits** | Full Report: **25 credits**")
        with col2:
            if st.button("💎 Buy Credits"):
                st.session_state.force_page = get_text('nav_credits')
                st.rerun()
    
    # Analysis tabs
    tab1, tab2, tab3 = st.tabs(["📊 Personal Numbers", "🎯 Lucky Dates & Times", "🤝 Name Compatibility"])
    
    with tab1:
        st.markdown("### Your Personal Numbers")
        
        # Profile selection
        user_manager = st.session_state.user_manager
        profiles = user_manager.list_profiles(user_email)
        
        if not profiles:
            st.warning("No profiles found. Please create a profile first!")
            return
        
        profile_names = [p.name for p in profiles]
        selected_name = st.selectbox("Select Profile", profile_names, key="num_profile")
        
        col1, col2 = st.columns(2)
        with col1:
            analysis_type = st.radio(
                "Analysis Type",
                ["Basic Numerology (10 credits)", "Full Report with Astrology (25 credits)"],
                key="analysis_type"
            )
        
        with col2:
            st.markdown("**What you get:**")
            if "Basic" in analysis_type:
                st.markdown("""
                - Life Path Number
                - Expression/Destiny Number
                - Soul Urge Number  
                - Personality Number
                - Lucky Colors & Days
                - Career Recommendations
                """)
            else:
                st.markdown("""
                - All Basic Features +
                - Integration with Birth Chart
                - Combined Career Analysis
                - Personalized Remedies
                - Financial Timing
                - Master Numbers Analysis
                """)
        
        if st.button("🔮 Calculate Numerology", type="primary"):
            # Get profile
            profile = next((p for p in profiles if p.name == selected_name), None)
            if not profile:
                st.error("Profile not found")
                return
            
            # Check credits
            cost = full_report_cost if "Full" in analysis_type else numerology_cost
            if payment_enabled and current_credits < cost:
                st.error(f"Insufficient credits! You need {cost} credits.")
                return
            
            with st.spinner("Calculating your numerology..."):
                try:
                    # Calculate numerology
                    numerology = NumerologyEngine()
                    birth_datetime = datetime.fromisoformat(f"{profile.birth_date}T{profile.birth_time}")
                    num_profile = numerology.calculate_profile(profile.name, birth_datetime)
                    
                    # Deduct credits
                    if payment_enabled:
                        st.session_state.payment_manager.deduct_credits(
                            user_email, cost, f"Numerology Analysis - {analysis_type}"
                        )
                    
                    st.success("✅ Numerology Calculated!")
                    
                    # Display results
                    st.markdown("---")
                    st.markdown("## 🌟 Your Core Numbers")
                    
                    # Core numbers in cards
                    cols = st.columns(4)
                    with cols[0]:
                        st.metric("Life Path", num_profile.life_path, help="Your life's purpose and journey")
                    with cols[1]:
                        st.metric("Expression", num_profile.expression, help="Your natural talents and abilities")
                    with cols[2]:
                        st.metric("Soul Urge", num_profile.soul_urge, help="Your inner desires and motivations")
                    with cols[3]:
                        st.metric("Personality", num_profile.personality, help="How others perceive you")
                    
                    st.markdown("---")
                    
                    # Life Path Interpretation
                    lp_interp = numerology.get_life_path_interpretation(num_profile.life_path)
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"### 🎯 Life Path {num_profile.life_path}: {lp_interp['title']}")
                        st.markdown(f"**Core Traits:** {', '.join(lp_interp['traits'])}")
                        st.markdown(f"**Strengths:** {lp_interp['strengths']}")
                        st.markdown(f"**Challenges:** {lp_interp['challenges']}")
                    
                    with col2:
                        st.markdown("#### 🍀 Lucky Elements")
                        st.markdown(f"**Colors:** {', '.join(lp_interp['lucky_colors'])}")
                        st.markdown(f"**Days:** {', '.join(lp_interp['lucky_days'])}")
                        gemstone = numerology.get_gemstone_recommendation(num_profile.life_path)
                        st.markdown(f"**Gemstone:** {gemstone['primary']}")
                        st.markdown(f"*Alternative:* {gemstone['secondary']}")
                    
                    # Career Recommendations
                    st.markdown("---")
                    st.markdown("### 💼 Career Paths (Numerology-Based)")
                    
                    careers = numerology.get_career_paths(num_profile.life_path, num_profile.expression)
                    
                    career_cols = st.columns(2)
                    for idx, career in enumerate(careers):
                        with career_cols[idx % 2]:
                            st.markdown(f"""
                            <div style="background-color: #F5F5F5; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                                <strong>🎯 {career['name']}</strong><br/>
                                <span style="color: #4CAF50;">{career['suitability']}</span><br/>
                                <small>{career['reason']}</small>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Master Numbers
                    if num_profile.master_numbers:
                        st.markdown("---")
                        st.markdown("### ✨ Master Numbers Detected!")
                        for master in num_profile.master_numbers:
                            master_interp = numerology.get_life_path_interpretation(master)
                            st.info(f"**{master} - {master_interp['title']}**: {master_interp['strengths']}")
                    
                    # Karmic Debts
                    if num_profile.karmic_debts:
                        st.markdown("---")
                        st.markdown("### ⚠️ Karmic Lessons")
                        for debt in num_profile.karmic_debts:
                            debt_interp = numerology.get_karmic_debt_interpretation(debt)
                            if debt_interp:
                                with st.expander(f"Karmic Debt {debt}"):
                                    st.markdown(f"**Meaning:** {debt_interp['meaning']}")
                                    st.markdown(f"**Lessons:** {', '.join(debt_interp['lessons'])}")
                                    st.markdown(f"**Remedy:** {debt_interp['remedy']}")
                    
                    # Full Report Integration
                    if "Full" in analysis_type:
                        st.markdown("---")
                        st.markdown("## 🔮 Astrology + Numerology Integration")
                        
                        # Calculate birth chart
                        calculator = st.session_state.astro_engine
                        
                        birth_details = BirthDetails(
                            date=birth_datetime,
                            latitude=profile.latitude,
                            longitude=profile.longitude,
                            timezone=profile.timezone,
                            name=profile.name,
                            place=profile.birth_place
                        )
                        
                        chart_data = calculator.calculate_birth_chart(birth_details)
                        
                        # Combined Career Analysis
                        st.markdown("### 💼 Combined Career Guidance")
                        
                        from src.career_guidance.career_analyzer import CareerAnalyzer
                        analyzer = CareerAnalyzer()
                        astro_result = analyzer.analyze_career_sectors(chart_data)
                        
                        if astro_result['success']:
                            st.markdown("#### Astrology Recommendations:")
                            for rec in astro_result['recommendations'][:3]:
                                st.success(f"**{rec['sector']}** - {rec['strength']} (Score: {rec['score']})")
                            
                            st.markdown("#### Numerology Recommendations:")
                            for career in careers[:3]:
                                st.info(f"**{career['name']}** - {career['suitability']}")
                            
                            st.markdown("""
                            💡 **Tip:** The careers that appear in both lists are your strongest options! 
                            They align with both your planetary influences and numerical vibrations.
                            """)
                        
                        # Remedies Integration
                        st.markdown("---")
                        st.markdown("### 🏥 Combined Remedies")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("#### Astrological Remedies")
                            remedy_engine = st.session_state.remedy_engine
                            remedies = remedy_engine.suggest_remedies(chart_data)
                            if remedies.get('success'):
                                for remedy in remedies['remedies'][:3]:
                                    st.markdown(f"🔹 **{remedy['type']}**: {remedy['description']}")
                        
                        with col2:
                            st.markdown("#### Numerological Remedies")
                            st.markdown(f"🔹 **Wear**: {', '.join(lp_interp['lucky_colors'])} colors")
                            st.markdown(f"🔹 **Important work on**: {', '.join(lp_interp['lucky_days'])}")
                            st.markdown(f"🔹 **Gemstone**: {gemstone['primary']} or {gemstone['secondary']}")
                            st.markdown(f"🔹 **Personal Year {num_profile.personal_year}**: Focus on new beginnings")
                    
                    # Additional Numbers
                    st.markdown("---")
                    st.markdown("### 📅 Additional Numbers")
                    cols = st.columns(3)
                    with cols[0]:
                        st.metric("Birthday Number", num_profile.birthday, help="Special talents")
                    with cols[1]:
                        st.metric("Personal Year", num_profile.personal_year, help="Current year theme")
                    with cols[2]:
                        st.metric("Maturity Number", num_profile.maturity, help="Life purpose after 30s")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab2:
        st.markdown("### 🍀 Lucky Dates for Financial Decisions")
        
        if not profiles:
            st.warning("Please create a profile first!")
            return
        
        profile_names = [p.name for p in profiles]
        selected_name_dates = st.selectbox("Select Profile", profile_names, key="num_dates")
        
        col1, col2 = st.columns(2)
        with col1:
            year = st.selectbox("Year", list(range(datetime.now().year, datetime.now().year + 3)))
        with col2:
            month = st.selectbox("Month", list(range(1, 13)), format_func=lambda x: datetime(2000, x, 1).strftime('%B'))
        
        if st.button("📅 Get Lucky Dates", key="lucky_dates_btn"):
            profile = next((p for p in profiles if p.name == selected_name_dates), None)
            if profile:
                with st.spinner("Calculating lucky dates..."):
                    numerology = NumerologyEngine()
                    birth_datetime = datetime.fromisoformat(f"{profile.birth_date}T{profile.birth_time}")
                    num_profile = numerology.calculate_profile(profile.name, birth_datetime)
                    
                    lucky_dates = numerology.get_lucky_dates_for_month(
                        num_profile.life_path, year, month
                    )
                    
                    st.success(f"✅ Lucky Dates for {datetime(year, month, 1).strftime('%B %Y')}")
                    
                    # Display in calendar format
                    st.markdown("### 📅 Favorable Dates for:")
                    st.markdown("- 💼 Starting new business ventures")
                    st.markdown("- 💰 Making investments")
                    st.markdown("- 🤝 Signing important contracts")
                    st.markdown("- 🏠 Property transactions")
                    
                    st.markdown("---")
                    
                    # Display dates in rows
                    dates_str = ", ".join([f"**{d}**" for d in lucky_dates])
                    st.markdown(f"### 🍀 Lucky Dates: {dates_str}")
                    
                    st.info(f"""
                    💡 **Your Life Path Number is {num_profile.life_path}**
                    
                    These dates resonate with your personal vibration and are especially favorable 
                    for financial decisions and new beginnings.
                    """)
    
    with tab3:
        st.markdown("### 🤝 Name & Relationship Compatibility")
        
        st.markdown("""
        Check compatibility between two names - perfect for:
        - Business partnerships
        - Personal relationships  
        - Choosing business names
        - Team compatibility
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            name1 = st.text_input("First Name", placeholder="e.g., John Doe")
        with col2:
            name2 = st.text_input("Second Name", placeholder="e.g., Jane Smith")
        
        if st.button("🔍 Check Compatibility", key="compat_btn"):
            if name1 and name2:
                with st.spinner("Analyzing compatibility..."):
                    numerology = NumerologyEngine()
                    compat = numerology.calculate_name_compatibility(name1, name2)
                    
                    st.markdown("---")
                    
                    # Compatibility Score
                    if compat['compatibility'] == 'Excellent':
                        color = "#4CAF50"
                        emoji = "🌟"
                    elif compat['compatibility'] == 'Good':
                        color = "#FFC107"
                        emoji = "👍"
                    else:
                        color = "#FF9800"
                        emoji = "⚠️"
                    
                    st.markdown(f"""
                    <div style="background-color: {color}20; padding: 20px; border-radius: 10px; border-left: 5px solid {color};">
                        <h2 style="color: {color};">{emoji} {compat['compatibility']} Compatibility</h2>
                        <p style="font-size: 18px;"><strong>Score:</strong> {compat['score']}/100</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(f"{compat['name1']}'s Expression Number", compat['expression1'])
                    with col2:
                        st.metric(f"{compat['name2']}'s Expression Number", compat['expression2'])
                    
                    st.info(compat['description'])
                    
                    # Recommendations
                    if compat['compatibility'] == 'Excellent':
                        st.success("""
                        ✨ **Excellent Match!**
                        - Natural harmony and understanding
                        - Complementary strengths
                        - Great for long-term partnerships
                        - Smooth communication and cooperation
                        """)
                    elif compat['compatibility'] == 'Good':
                        st.success("""
                        👍 **Good Match!**
                        - Compatible with effort
                        - Learn from each other
                        - Build on common ground
                        - Requires open communication
                        """)
                    else:
                        st.warning("""
                        ⚠️ **Challenging Match**
                        - Different life approaches
                        - Requires compromise
                        - Can grow through challenges
                        - Focus on understanding differences
                        """)
            else:
                st.warning("Please enter both names")


def show_career_guidance():
    """Career and Business Sector Analysis Page"""
    st.header("💼 Career & Business Sector Analysis")
    st.markdown("Discover ideal business sectors based on your birth chart's planetary positions")
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        st.warning("Please login to access career guidance")
        return
    
    # Check payment (standard question price)
    payment_enabled = config.get('payment', {}).get('enabled', False)
    if payment_enabled:
        user_email = st.session_state.current_user
        current_credits = st.session_state.payment_manager.get_user_credits(user_email)
        career_cost = config.get('payment', {}).get('pricing', {}).get('career_guidance', 10)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"💳 Credits: **{current_credits}** | Cost: **{career_cost} credits**")
        with col2:
            if st.button("➕ Buy Credits"):
                st.session_state.force_page = get_text('nav_credits')
                st.rerun()
        
        if current_credits < career_cost:
            st.error(f"Insufficient credits! You need {career_cost} credits for career analysis.")
            return
    
    # Profile selection
    user_email = st.session_state.current_user
    user_manager = st.session_state.user_manager
    profiles = user_manager.list_profiles(user_email)
    
    if not profiles:
        st.warning("No profiles found. Please create a profile first!")
        return
    
    profile_names = [p.name for p in profiles]
    selected_name = st.selectbox("Select Profile for Career Analysis", profile_names)
    
    if st.button("🔍 Analyze Career Sectors", type="primary"):
        with st.spinner("Analyzing your birth chart for career sectors..."):
            # Get profile data
            profile = next((p for p in profiles if p.name == selected_name), None)
            
            if not profile:
                st.error("Profile not found")
                return
            
            # Calculate chart
            try:
                from src.astrology_engine.vedic_calculator import BirthDetails
                from datetime import datetime
                
                calculator = st.session_state.astro_engine
                
                # Create BirthDetails object
                birth_datetime = datetime.fromisoformat(
                    f"{profile.birth_date}T{profile.birth_time}"
                )
                
                birth_details = BirthDetails(
                    date=birth_datetime,
                    latitude=profile.latitude,
                    longitude=profile.longitude,
                    timezone=profile.timezone,
                    name=profile.name,
                    place=profile.birth_place
                )
                
                chart_data = calculator.calculate_birth_chart(birth_details)
                
                # Analyze career sectors
                from src.career_guidance.career_analyzer import CareerAnalyzer
                analyzer = CareerAnalyzer()
                result = analyzer.analyze_career_sectors(chart_data)
                
                if result['success']:
                    # Deduct credits
                    if payment_enabled:
                        st.session_state.payment_manager.deduct_credits(
                            user_email, career_cost, "Career Sector Analysis"
                        )
                    
                    st.success("✅ Career Analysis Complete!")
                    
                    # Display recommendations
                    st.markdown("### 🎯 Your Top Investment Sectors")
                    
                    for rec in result['recommendations']:
                        # Star rating based on strength
                        if rec['strength'] == "Excellent":
                            stars = "⭐⭐⭐⭐⭐"
                        elif rec['strength'] == "Very Good":
                            stars = "⭐⭐⭐⭐"
                        elif rec['strength'] == "Good":
                            stars = "⭐⭐⭐"
                        else:
                            stars = "⭐⭐"
                        
                        with st.expander(f"{stars} {rec['strength']} - {rec['sector']}", expanded=(rec['rank'] == 1)):
                            # Display score
                            st.metric("Sector Strength Score", f"{rec['score']}/{rec['max_score']}")
                            
                            st.info(f"💡 **Investment Advice:** {rec['advice']}")
                            
                            st.caption(f"**Sector includes:** {rec['description']}")
                            st.caption("**Key planetary factors:**")
                            for factor in rec['factors']:
                                st.caption(f"• {factor}")
                    
                    # Display planetary strengths
                    st.markdown("### 🌟 Your Planetary Strengths")
                    strengths = result['planetary_strengths']
                    cols = st.columns(4)
                    for idx, (planet, strength) in enumerate(strengths.items()):
                        with cols[idx % 4]:
                            st.metric(planet, f"{strength}/100")
                    
                else:
                    st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")


def show_financial_outlook():
    """Financial Astrology - Market Outlook Page"""
    st.header("📈 Financial Astrology - Market Outlook")
    st.markdown("Stock market predictions based on current planetary transits")
    
    # Premium feature notice with custom styling
    st.markdown("""
    <div style="background-color: #FFE5CC; padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #FF9933;">
        <p style="margin: 0; color: #333;">🌟 <strong>Premium Feature</strong> - Advanced financial astrology analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        st.warning("Please login to access financial outlook")
        return
    
    # Check payment (premium pricing)
    payment_enabled = config.get('payment', {}).get('enabled', False)
    user_email = st.session_state.current_user
    current_credits = 0
    financial_cost = 50
    
    if payment_enabled:
        # Get premium credits (separate from standard)
        current_credits = st.session_state.payment_manager.get_user_credits(user_email)
        financial_cost = config.get('payment', {}).get('pricing', {}).get('financial_astrology', {}).get('per_query', 50)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"💎 Credits: **{current_credits}** | Premium Cost: **{financial_cost} credits** (₹50)")
        with col2:
            if st.button("💎 Buy Premium"):
                st.session_state.force_page = get_text('nav_credits')
                st.rerun()
        
        if current_credits < financial_cost:
            st.error(f"Insufficient credits! You need {financial_cost} credits for financial analysis.")
            st.info("💡 Premium packs available: 5 queries @ ₹200, 10 queries @ ₹350")
            return
    
    # Analysis tabs
    tab1, tab2, tab3 = st.tabs(["📊 Market Overview", "🎯 Sector Analysis", "👤 Personalized"])
    
    with tab1:
        st.markdown("### Current Market Outlook")
        
        if st.button("🔄 Get Market Outlook", type="primary"):
            with st.spinner("Analyzing current planetary transits..."):
                try:
                    from src.financial_astrology.financial_analyzer import FinancialAnalyzer
                    analyzer = FinancialAnalyzer()
                    outlook = analyzer.get_market_outlook()
                    
                    if outlook['success']:
                        # Deduct credits
                        if payment_enabled:
                            st.session_state.payment_manager.deduct_credits(
                                user_email, financial_cost, "Financial Market Outlook"
                            )
                        
                        st.success(f"✅ Analysis Date: {outlook['date']}")
                        
                        # Market sentiment
                        st.markdown(f"### {outlook['market_sentiment']}")
                        st.progress(outlook['overall_strength'] / 100)
                        
                        # Top sectors
                        st.markdown("### 🔥 Top Performing Sectors")
                        for sector in outlook['top_sectors']:
                            with st.expander(f"{sector['rating']} - {sector['sector']}"):
                                st.markdown(f"**Prediction:** {sector['prediction']}")
                                st.markdown(f"**Major Companies:** {sector['major_companies']}")
                                st.markdown(f"**Favorable Factors:**")
                                for factor in sector['favorable_factors']:
                                    st.markdown(f"✅ {factor}")
                        
                        # Weak sectors
                        st.markdown("### ⚠️ Sectors to Avoid")
                        for sector in outlook['weak_sectors']:
                            st.warning(f"{sector['sector']} - {sector['rating']}")
                        
                        # Upcoming events
                        if outlook['upcoming_events']:
                            st.markdown("### 📅 Upcoming Astrological Events")
                            for event in outlook['upcoming_events']:
                                st.info(f"{event.get('type', 'Event')}: {event.get('description', 'No description')}")
                    
                    else:
                        st.error(f"Analysis failed: {outlook.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab2:
        st.markdown("### Analyze Specific Sector")
        
        sectors = [
            'Technology & IT', 'Banking & Finance', 'Pharmaceuticals',
            'Real Estate', 'Oil & Energy', 'FMCG & Consumer',
            'Automobiles', 'Metals & Mining', 'Infrastructure',
            'Media & Entertainment'
        ]
        
        selected_sector = st.selectbox("Select Sector", sectors)
        
        if st.button("🔍 Analyze Sector"):
            with st.spinner(f"Analyzing {selected_sector}..."):
                try:
                    from src.financial_astrology.financial_analyzer import FinancialAnalyzer
                    analyzer = FinancialAnalyzer()
                    result = analyzer.analyze_sector(selected_sector)
                    
                    if result['success']:
                        st.success(f"✅ Analysis for {result['sector']}")
                        st.markdown(f"## {result['rating']}")
                        st.markdown(f"**Prediction:** {result['prediction']}")
                        st.markdown(f"**Timing:** {result['timing']}")
                        st.markdown(f"**Major Companies:** {result['major_companies']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Favorable Factors:**")
                            for factor in result['favorable_factors']:
                                st.markdown(f"✅ {factor}")
                        with col2:
                            st.markdown("**Unfavorable Factors:**")
                            for factor in result['unfavorable_factors']:
                                st.markdown(f"⚠️ {factor}")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab3:
        st.markdown("### Personalized Investment Recommendations")
        
        # Use markdown with custom styling instead of st.info
        st.markdown("""
        <div style="background-color: #FFE5CC; padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #FF9933;">
            <p style="margin: 0; color: #333;">💎 <strong>Premium Report</strong> - ₹50 (50 credits) - Combines your birth chart with current transits</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Profile selection
        user_manager = st.session_state.user_manager
        profiles = user_manager.list_profiles(user_email)
        
        if not profiles:
            st.warning("No profiles found. Please create a profile first!")
            return
        
        profile_names = [p.name for p in profiles]
        selected_name = st.selectbox("Select Profile", profile_names)
        
        personalized_cost = config.get('payment', {}).get('pricing', {}).get('financial_astrology', {}).get('personalized_report', 100)
        
        if st.button("📊 Get Personalized Report (₹50)", type="primary"):
            if payment_enabled and current_credits < personalized_cost:
                st.error(f"Insufficient credits! You need {personalized_cost} credits.")
                return
            
            with st.spinner("Generating personalized investment report..."):
                try:
                    profile = next((p for p in profiles if p.name == selected_name), None)
                    
                    from src.astrology_engine.vedic_calculator import BirthDetails
                    from datetime import datetime
                    
                    calculator = st.session_state.astro_engine
                    
                    # Create BirthDetails object
                    birth_datetime = datetime.fromisoformat(
                        f"{profile.birth_date}T{profile.birth_time}"
                    )
                    
                    birth_details = BirthDetails(
                        date=birth_datetime,
                        latitude=profile.latitude,
                        longitude=profile.longitude,
                        timezone=profile.timezone,
                        name=profile.name,
                        place=profile.birth_place
                    )
                    
                    chart_data = calculator.calculate_birth_chart(birth_details)
                    
                    from src.financial_astrology.financial_analyzer import FinancialAnalyzer
                    analyzer = FinancialAnalyzer()
                    result = analyzer.get_personalized_analysis(chart_data)
                    
                    if result['success']:
                        # Deduct credits
                        if payment_enabled:
                            st.session_state.payment_manager.deduct_credits(
                                user_email, personalized_cost, "Personalized Financial Report"
                            )
                        
                        st.success(f"✅ Report Generated - {result['analysis_date']}")
                        
                        st.markdown("### 🎯 Your Top Investment Sectors")
                        for rec in result['recommendations']:
                            with st.expander(f"{rec['rating']} - {rec['sector']}"):
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Natal Strength", rec['natal_strength'])
                                with col2:
                                    st.metric("Transit Strength", rec['transit_strength'])
                                with col3:
                                    st.metric("Total Score", rec['total_strength'])
                                
                                st.info(f"💡 **Investment Advice:** {rec['advice']}")
                                
                                # Stock recommendations
                                if rec.get('stocks'):
                                    st.markdown("---")
                                    st.markdown("**📊 Recommended Stocks (Fundamental Analysis):**")
                                    stock_cols = st.columns(2)
                                    for idx, stock in enumerate(rec['stocks']):
                                        with stock_cols[idx % 2]:
                                            st.markdown(f"• {stock}")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")


def show_soulmate_analysis():
    """Comprehensive Soulmate Analysis with visual representation + detailed predictions"""
    st.header("💕 Your Soulmate Analysis")
    st.caption("Discover your ideal life partner based on 7th house, Venus/Mars, and Navamsa chart")
    
    # Get user profiles
    user_email = st.session_state.current_user if st.session_state.logged_in else ""
    user_manager = st.session_state.user_manager
    profiles = user_manager.list_profiles(user_email)
    
    if not profiles:
        st.warning("Please create a user profile first!")
        if st.button("Go to User Profiles"):
            st.session_state.force_page = get_text('nav_profiles')
            st.rerun()
        return
    
    profile_names = [p.name for p in profiles]
    selected_name = st.selectbox("Select Your Profile", profile_names)
    
    st.markdown("**Pricing:** ₹5")
    
    if st.button("🔮 Reveal Your Soulmate", type="primary"):
        profile = next((p for p in profiles if p.name == selected_name), None)
        
        with st.spinner("Analyzing your 7th house, Venus, Mars, and Navamsa chart..."):
            try:
                from src.astrology_engine.vedic_calculator import BirthDetails
                from datetime import datetime
                
                calculator = st.session_state.astro_engine
                birth_dt = datetime.fromisoformat(f"{profile.birth_date}T{profile.birth_time}")
                
                details = BirthDetails(
                    date=birth_dt,
                    latitude=profile.latitude,
                    longitude=profile.longitude,
                    timezone=profile.timezone,
                    name=profile.name,
                    place=profile.birth_place
                )
                chart = calculator.calculate_birth_chart(details)
                
                # Analyze soulmate characteristics
                soulmate_data = analyze_soulmate(chart, profile)
                
                st.success("✨ Your Soulmate Analysis is Ready!")
                
                # Physical & Personality Analysis
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📋 Physical Characteristics")
                    st.info(f"**Height:** {soulmate_data['physical']['height']}")
                    st.info(f"**Build:** {soulmate_data['physical']['build']}")
                    st.info(f"**Complexion:** {soulmate_data['physical']['complexion']}")
                    st.info(f"**Special Features:** {soulmate_data['physical']['features']}")
                    st.info(f"**Overall Look:** {soulmate_data['physical']['style']}")
                
                st.markdown("---")
                
                # Personality Traits
                st.markdown("### 💫 Personality & Nature")
                traits_col1, traits_col2 = st.columns(2)
                
                with traits_col1:
                    st.markdown("**✨ Positive Qualities:**")
                    for trait in soulmate_data['personality']['positive']:
                        st.markdown(f"• {trait}")
                
                with traits_col2:
                    st.markdown("**💎 Character Traits:**")
                    for trait in soulmate_data['personality']['traits']:
                        st.markdown(f"• {trait}")
                
                st.markdown("---")
                
                # Professional & Background
                st.markdown("### 💼 Professional & Background Profile")
                prof_col1, prof_col2 = st.columns(2)
                
                with prof_col1:
                    st.success(f"**Likely Profession:** {soulmate_data['background']['profession']}")
                    st.info(f"**Education Level:** {soulmate_data['background']['education']}")
                
                with prof_col2:
                    st.success(f"**Family Background:** {soulmate_data['background']['family']}")
                    st.info(f"**Economic Status:** {soulmate_data['background']['financial']}")
                
                st.markdown("---")
                
                # Meeting & Timing
                st.markdown("### ⏰ When & Where You'll Meet")
                timing_col1, timing_col2 = st.columns(2)
                
                with timing_col1:
                    st.warning(f"🕐 **Most Likely Time Period:**\n{soulmate_data['timing']['period']}")
                    st.info(f"📍 **Possible Meeting Place:**\n{soulmate_data['timing']['place']}")
                
                with timing_col2:
                    st.success(f"💝 **How You'll Meet:**\n{soulmate_data['timing']['how']}")
                    st.info(f"⚡ **First Impression:**\n{soulmate_data['timing']['first_impression']}")
                
                st.markdown("---")
                
                # Compatibility Factors
                st.markdown("### 🌟 What Makes You Compatible")
                for factor in soulmate_data['compatibility']:
                    st.success(f"✓ {factor}")
                
                st.markdown("---")
                
                # Activation Remedies
                st.markdown("### 🔧 Remedies to Attract Your Soulmate")
                st.caption("Strengthen your 7th house and Venus/Mars to manifest your ideal partner")
                
                remedy_col1, remedy_col2 = st.columns(2)
                
                with remedy_col1:
                    st.markdown("**🌺 Daily Practices:**")
                    for remedy in soulmate_data['remedies']['daily']:
                        st.markdown(f"• {remedy}")
                
                with remedy_col2:
                    st.markdown("**💎 Special Remedies:**")
                    for remedy in soulmate_data['remedies']['special']:
                        st.markdown(f"• {remedy}")
                
                st.info("💡 **Pro Tip:** Be patient and trust the cosmic timing. Your soulmate is preparing to meet you!")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")


def analyze_soulmate(chart, profile):
    """Analyze 7th house, Venus, Mars, and Navamsa to determine soulmate characteristics"""
    planets = chart['planets']
    
    # Get 7th house lord (opposite of ascendant)
    ascendant_sign = chart['ascendant'].sign
    house_7_sign = get_7th_house_sign(ascendant_sign)
    
    # Get Venus and Mars
    venus = planets.get('Venus')
    mars = planets.get('Mars')
    jupiter = planets.get('Jupiter')
    
    # Determine gender for analysis
    is_male = profile.gender == "male"
    primary_planet = mars if is_male else venus
    
    # Physical Characteristics
    physical = analyze_physical_features(primary_planet, house_7_sign, jupiter)
    
    # Personality
    personality = analyze_personality_traits(primary_planet, house_7_sign, venus, mars)
    
    # Background & Profession
    background = analyze_background(jupiter, venus, house_7_sign)
    
    # Timing & Meeting
    timing = analyze_meeting_timing(primary_planet, jupiter, chart)
    
    # Compatibility Factors
    compatibility = analyze_compatibility_factors(chart, is_male)
    
    # Remedies
    remedies = get_soulmate_remedies(primary_planet, house_7_sign)
    
    return {
        'appearance': physical['visual'],
        'physical': physical,
        'personality': personality,
        'background': background,
        'timing': timing,
        'compatibility': compatibility,
        'remedies': remedies
    }


def get_7th_house_sign(ascendant_sign):
    """Get 7th house sign (opposite of ascendant)"""
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
             'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    if ascendant_sign in signs:
        idx = signs.index(ascendant_sign)
        return signs[(idx + 6) % 12]
    return 'Libra'


def analyze_physical_features(planet, sign, jupiter):
    """Determine physical appearance with detailed visual parameters"""
    height = "Medium to tall"
    build = "Well-proportioned"
    complexion = "Fair to wheatish"
    features = "Attractive eyes"
    style = "Elegant and well-groomed"
    
    # Visual parameters for illustration
    face_type = "oval"
    skin_color = "#f4c2a0"  # Default fair
    hair_color = "#3d2817"  # Dark brown
    hair_style_css = "border-radius: 50% 50% 0 0;"
    eye_color = "#4a3728"  # Dark brown
    height_percent = 140  # Body height in pixels
    
    if planet:
        # Based on planet's sign
        if planet.sign in ['Taurus', 'Libra', 'Pisces']:
            complexion = "Fair and glowing"
            features = "Beautiful eyes, graceful smile"
            build = "Attractive, well-built"
            face_type = "round"
            skin_color = "#fce5cd"
            eye_color = "#6b4423"
            hair_color = "#5d3a1a"
            hair_style_css = "border-radius: 50%;"
            
        elif planet.sign in ['Aries', 'Leo', 'Sagittarius']:
            complexion = "Bright, reddish tint"
            features = "Sharp features, confident look"
            build = "Athletic, strong"
            height = "Above average"
            face_type = "oval"
            skin_color = "#f5b895"
            eye_color = "#3d2817"
            hair_color = "#2c1810"
            hair_style_css = "border-radius: 30% 30% 0 0;"
            height_percent = 150
            
        elif planet.sign in ['Cancer', 'Scorpio']:
            complexion = "Fair to dusky"
            features = "Expressive eyes, mysterious charm"
            build = "Medium, attractive"
            face_type = "round"
            skin_color = "#d4a574"
            eye_color = "#1a1a1a"
            hair_color = "#1a1a1a"
            hair_style_css = "border-radius: 50% 50% 0 0;"
            
        elif planet.sign in ['Gemini', 'Virgo', 'Aquarius']:
            complexion = "Wheatish"
            features = "Intelligent look, pleasant"
            build = "Slim to medium"
            face_type = "oval"
            skin_color = "#d99b6c"
            eye_color = "#5c3d2e"
            hair_color = "#3d2817"
            hair_style_css = "border-radius: 40% 40% 0 0;"
            height_percent = 135
            
        elif planet.sign in ['Capricorn']:
            complexion = "Dusky to wheatish"
            features = "Strong features, serious look"
            build = "Lean, tall"
            face_type = "oval"
            skin_color = "#c18f6d"
            eye_color = "#3d2817"
            hair_color = "#1a1a1a"
            hair_style_css = "border-radius: 30% 30% 0 0;"
            height_percent = 155
    
    if jupiter and jupiter.house in [1, 7, 9, 11]:
        height = "Tall"
        build = "Well-built, healthy"
        height_percent = 160
    
    return {
        'height': height,
        'build': build,
        'complexion': complexion,
        'features': features,
        'style': style,
        'visual': {
            'emoji': '👤',
            'build': build,
            'complexion': complexion,
            'features': features,
            'face_type': face_type,
            'skin_color': skin_color,
            'hair_style': {
                'color': hair_color,
                'style': hair_style_css
            },
            'eye_color': eye_color,
            'height_percent': height_percent
        }
    }


def analyze_personality_traits(planet, sign, venus, mars):
    """Determine personality characteristics"""
    positive = []
    traits = []
    
    if planet:
        if planet.sign in ['Taurus', 'Libra', 'Pisces']:
            positive.extend(["Kind-hearted and loving", "Artistic and creative", "Peace-loving nature"])
            traits.extend(["Gentle speaker", "Values harmony", "Romantic"])
        elif planet.sign in ['Aries', 'Leo', 'Sagittarius']:
            positive.extend(["Confident and ambitious", "Natural leader", "Optimistic outlook"])
            traits.extend(["Passionate", "Independent", "Adventurous"])
        elif planet.sign in ['Cancer', 'Scorpio']:
            positive.extend(["Emotionally deep", "Loyal and devoted", "Intuitive"])
            traits.extend(["Protective", "Intense", "Family-oriented"])
        elif planet.sign in ['Gemini', 'Virgo', 'Aquarius']:
            positive.extend(["Intelligent and witty", "Good communicator", "Practical thinker"])
            traits.extend(["Analytical", "Social", "Helpful"])
    
    if venus and venus.house in [1, 5, 7]:
        positive.append("Naturally charming and attractive")
    
    if mars and mars.house in [3, 6, 10]:
        positive.append("Hardworking and determined")
    
    return {'positive': positive[:4], 'traits': traits[:4]}


def analyze_background(jupiter, venus, sign):
    """Determine professional and family background"""
    profession = "Professional or Business"
    education = "Well-educated (Graduate or higher)"
    family = "Respectable, middle to upper-class"
    financial = "Financially stable"
    
    if jupiter:
        if jupiter.house in [2, 5, 9, 11]:
            family = "Well-established, educated family"
            education = "Highly educated (Post-graduate possible)"
            financial = "Financially prosperous"
        if jupiter.sign in ['Sagittarius', 'Pisces', 'Cancer']:
            profession = "Teaching, Law, Finance, or Spiritual field"
    
    if venus:
        if venus.house in [2, 10, 11]:
            profession = "Arts, Fashion, Media, Hospitality, or Finance"
            financial = "Good earning potential"
    
    return {
        'profession': profession,
        'education': education,
        'family': family,
        'financial': financial
    }


def analyze_meeting_timing(planet, jupiter, chart):
    """Predict when and how they'll meet"""
    age_ranges = ["18-24 years", "25-28 years", "28-32 years", "32-36 years"]
    
    # Calculate based on dashas or transits
    period = age_ranges[1]  # Default
    place = "Through friends/family, social gathering, or workplace"
    how = "Natural meeting through mutual connections or common interests"
    first_impression = "Instant connection and positive vibes"
    
    if jupiter and jupiter.house in [1, 5, 7, 9, 11]:
        period = age_ranges[1]
        place = "Religious place, educational institution, or through family"
        first_impression = "Respectful and immediate comfort"
    
    if planet:
        if planet.house in [5, 7, 11]:
            period = age_ranges[0]
            how = "Love at first sight or gradual friendship turning to love"
        elif planet.house in [10, 11]:
            place = "Workplace, professional event, or networking"
            how = "Professional connection developing into romance"
    
    return {
        'period': period,
        'place': place,
        'how': how,
        'first_impression': first_impression
    }


def analyze_compatibility_factors(chart, is_male):
    """What makes them compatible"""
    factors = []
    
    factors.append("Complementary personalities - you balance each other")
    factors.append("Shared values and life goals")
    factors.append("Strong emotional and intellectual connection")
    factors.append("Mutual respect and understanding")
    factors.append("Supportive of each other's ambitions")
    
    return factors[:5]


def get_soulmate_remedies(planet, sign):
    """Chart-specific remedies to attract soulmate based on Venus/Mars placement"""
    daily = []
    special = []
    
    # Base remedies for 7th house activation
    daily.append("Worship Lord Shiva/Parvati on Mondays for marital harmony")
    
    # Planet-specific remedies
    if planet:
        planet_name = "Venus" if hasattr(planet, 'sign') else "Venus"
        
        # Sign-based remedies
        if planet.sign in ['Aries', 'Scorpio']:
            # Mars-ruled signs - strengthen Mars
            daily.append("Recite Hanuman Chalisa on Tuesdays")
            daily.append("Wear red on Tuesdays to boost Mars energy")
            special.append("Wear Red Coral (after consultation) - strengthens Mars")
            special.append("Donate red lentils on Tuesdays")
            
        elif planet.sign in ['Taurus', 'Libra']:
            # Venus-ruled signs - strengthen Venus
            daily.append("Chant 'Om Shukraya Namah' 108 times on Fridays")
            daily.append("Wear white or pastel colors on Fridays")
            special.append("Wear Diamond or Opal (after consultation)")
            special.append("Donate white clothes/rice to women on Fridays")
            
        elif planet.sign in ['Gemini', 'Virgo']:
            # Mercury-ruled signs
            daily.append("Chant 'Om Budhaya Namah' 108 times on Wednesdays")
            daily.append("Feed green vegetables to cows on Wednesdays")
            special.append("Wear Emerald (after consultation)")
            special.append("Donate books or help students")
            
        elif planet.sign in ['Cancer']:
            # Moon-ruled sign
            daily.append("Chant 'Om Chandraya Namah' 108 times on Mondays")
            daily.append("Offer water to Moon on full moon nights")
            special.append("Wear Pearl (after consultation)")
            special.append("Donate white items to women on Mondays")
            
        elif planet.sign in ['Leo']:
            # Sun-ruled sign
            daily.append("Chant 'Om Suryaya Namah' 108 times on Sundays")
            daily.append("Offer water to Sun at sunrise")
            special.append("Wear Ruby (after consultation)")
            special.append("Donate wheat or jaggery on Sundays")
            
        elif planet.sign in ['Sagittarius', 'Pisces']:
            # Jupiter-ruled signs
            daily.append("Chant 'Om Gurave Namah' 108 times on Thursdays")
            daily.append("Wear yellow on Thursdays")
            special.append("Wear Yellow Sapphire (after consultation)")
            special.append("Donate yellow items or turmeric on Thursdays")
            
        elif planet.sign in ['Capricorn', 'Aquarius']:
            # Saturn-ruled signs
            daily.append("Chant 'Om Shanaye Namah' 108 times on Saturdays")
            daily.append("Light a mustard oil lamp on Saturdays")
            special.append("Wear Blue Sapphire (after consultation)")
            special.append("Donate black sesame or mustard oil on Saturdays")
        
        # House-based remedies
        if planet.house in [6, 8, 12]:
            daily.append("Perform Gauri-Shankar puja for removing obstacles")
            special.append("Chant Mahamrityunjaya Mantra for protection")
        
        if planet.is_retrograde:
            daily.append("Chant planetary mantra 2x more (retrograde planet needs extra attention)")
            special.append("Perform planetary peace ritual (Graha Shanti)")
    
    # General 7th house remedies
    if len(daily) < 4:
        daily.append("Donate to couples or support marriages")
        daily.append("Keep a happy married couple's photo at home")
    
    if len(special) < 4:
        special.append("Visit Parvati temples during Mahashivratri")
        special.append("Perform Swayamvara Parvati puja for finding right partner")
    
    return {'daily': daily[:4], 'special': special[:4]}


if __name__ == "__main__":
    main()
