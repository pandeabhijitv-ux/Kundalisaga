# Career Guidance & Financial Astrology - Implementation Guide

## ✅ Completed Components

### 1. Career Guidance Module (`src/career_guidance/`)
- **File**: `career_analyzer.py` (360 lines)
- **Features**:
  - Analyzes 10th house (career), 2nd house (wealth), Ascendant
  - Maps 15 business sectors to planetary influences
  - Calculates planetary strengths (exaltation, own sign, retrograde)
  - Generates top 5 sector recommendations with scores and advice
  
- **Sectors Covered**:
  - IT & Technology (Mercury, Rahu)
  - Finance & Banking (Jupiter, Venus, Mercury)
  - Real Estate & Construction (Mars, Saturn)
  - Engineering & Manufacturing (Mars, Saturn)
  - Healthcare & Pharmaceuticals (Moon, Jupiter, Sun)
  - Education & Training (Jupiter, Mercury)
  - Arts & Entertainment (Venus, Moon)
  - Government & Administration (Sun, Saturn)
  - Agriculture & Food (Saturn, Moon, Venus)
  - Consulting & Advisory (Jupiter, Mercury)
  - Trade & Commerce (Mercury, Venus)
  - Energy & Mining (Sun, Mars)
  - Hospitality & Tourism (Venus, Moon)
  - Sports & Fitness (Mars, Sun)
  - Spiritual & Religious (Jupiter, Ketu)

### 2. Financial Astrology Module (`src/financial_astrology/`)

#### A. Transit Tracker (`transit_tracker.py`)
- Gets current planetary positions
- Calculates Moon phases
- Tracks retrograde periods
- Identifies upcoming eclipses
- Maps transits to market timing

#### B. Sector Predictor (`sector_predictor.py`)
- Maps 10 stock market sectors to planets:
  - Technology & IT → Mercury, Rahu
  - Banking & Finance → Jupiter, Venus
  - Pharmaceuticals → Moon, Jupiter
  - Real Estate → Mars, Saturn
  - Oil & Energy → Sun, Mars
  - FMCG & Consumer → Venus, Moon
  - Automobiles → Mars, Mercury
  - Metals & Mining → Saturn, Mars
  - Infrastructure → Saturn, Mars
  - Media & Entertainment → Venus, Mercury

- Analyzes transit impact on sectors
- Generates ⭐-based ratings
- Provides timing recommendations
- Lists major companies in each sector

#### C. Financial Analyzer (`financial_analyzer.py`)
- Main interface for financial predictions
- Combines transit + natal chart analysis
- Generates market outlook (Bullish 🟢/Neutral 🟡/Bearish 🔴)
- Personalized investment recommendations
- Sector-specific timing advice

### 3. Payment Configuration (`config/config.yaml`)

**Standard Features (₹10 per use)**:
- single_question: 10
- remedy_consultation: 10
- career_guidance: 10

**Premium Features - Financial Astrology**:
- per_query: ₹50 (general financial question)
- sector_analysis: ₹50 (detailed sector report)
- personalized_report: ₹100 (full investment recommendations)

**Premium Bulk Packs** (for Financial Astrology):
- 5 queries: ₹200 (₹40/query - save ₹10)
- 10 queries: ₹350 (₹35/query - save ₹15)
- 20 queries: ₹600 (₹30/query - save ₹20)

---

## 🔄 Pending Integration (Next Steps)

### Step 1: Add Translations to app.py

Add to TRANSLATIONS dictionary in app.py (around line 78):

```python
# In English section:
'nav_career': '💼 Career Guidance',
'nav_financial': '📈 Financial Outlook',

# Career Guidance
'career_title': 'Career & Business Sector Analysis',
'career_subtitle': 'Discover your ideal business sectors based on your birth chart',
'top_sectors': 'Top Recommended Sectors',
'sector_rank': 'Rank',
'sector_name': 'Sector',
'sector_strength': 'Strength',
'sector_factors': 'Key Factors',
'sector_advice': 'Advice',
'sector_description': 'Includes',

# Financial Astrology
'financial_title': 'Financial Astrology - Market Outlook',
'financial_subtitle': 'Stock market predictions based on planetary transits',
'market_sentiment': 'Overall Market Sentiment',
'current_strength': 'Market Strength',
'top_performing': 'Top Performing Sectors',
'weak_sectors': 'Sectors to Avoid',
'upcoming_events': 'Upcoming Astrological Events',
'sector_rating': 'Rating',
'timing_advice': 'Timing',
'major_stocks': 'Major Companies',
'premium_feature': 'Premium Feature',
'premium_credits_needed': 'Premium Credits Required',
'buy_premium_credits': 'Buy Premium Credits',
'personalized_recommendations': 'Personalized Investment Recommendations',
'get_personalized_report': 'Get Personalized Report (₹100)',
```

**Repeat for Hindi and Marathi sections**

### Step 2: Update Navigation (app.py line ~500)

```python
# Update nav_list to include new pages
if lang == 'Hindi':
    nav_list = [get_text('nav_home'), get_text('nav_profiles'), 
                get_text('nav_horoscope'), get_text('nav_ask'), 
                get_text('nav_remedies'), get_text('nav_career'),  # NEW
                get_text('nav_financial'),  # NEW
                get_text('nav_credits'), get_text('nav_settings')]
```

### Step 3: Add Page Routing (app.py line ~540)

```python
# Add after existing page routing:
elif page == get_text('nav_career'):
    show_career_guidance()
elif page == get_text('nav_financial'):
    show_financial_outlook()
```

### Step 4: Add Career Guidance Page Function

Add this function to app.py (before `if __name__ == "__main__":`):

```python
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
    profiles = user_manager.get_all_profiles(user_email)
    
    if not profiles:
        st.warning("No profiles found. Please create a profile first!")
        return
    
    profile_names = [p['name'] for p in profiles]
    selected_name = st.selectbox("Select Profile for Career Analysis", profile_names)
    
    if st.button("🔍 Analyze Career Sectors", type="primary"):
        with st.spinner("Analyzing your birth chart for career sectors..."):
            # Get profile data
            profile = next((p for p in profiles if p['name'] == selected_name), None)
            
            if not profile:
                st.error("Profile not found")
                return
            
            # Calculate chart
            try:
                from src.astrology_engine.vedic_calculator import VedicCalculator
                calculator = VedicCalculator()
                chart_data = calculator.calculate_birth_chart(
                    profile['birth_date'],
                    profile['birth_time'],
                    profile['latitude'],
                    profile['longitude']
                )
                
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
                    st.markdown("### 🎯 Top Recommended Sectors")
                    
                    for rec in result['recommendations']:
                        with st.expander(f"#{rec['rank']} - {rec['sector']} ({rec['strength']})", expanded=(rec['rank'] == 1)):
                            st.markdown(f"**Strength Score:** {rec['score']}/200")
                            st.markdown(f"**Includes:** {rec['description']}")
                            st.markdown(f"**Key Factors:**")
                            for factor in rec['factors']:
                                st.markdown(f"- {factor}")
                            st.info(f"💡 **Advice:** {rec['advice']}")
                    
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
```

### Step 5: Add Financial Outlook Page Function

```python
def show_financial_outlook():
    """Financial Astrology - Market Outlook Page"""
    st.header("📈 Financial Astrology - Market Outlook")
    st.markdown("Stock market predictions based on current planetary transits")
    
    # Premium feature notice
    st.warning("🌟 **Premium Feature** - Advanced financial astrology analysis")
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        st.warning("Please login to access financial outlook")
        return
    
    # Check payment (premium pricing)
    payment_enabled = config.get('payment', {}).get('enabled', False)
    user_email = st.session_state.current_user
    
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
        st.info("💎 **Premium Report** - ₹100 (100 credits) - Combines your birth chart with current transits")
        
        # Profile selection
        user_manager = st.session_state.user_manager
        profiles = user_manager.get_all_profiles(user_email)
        
        if not profiles:
            st.warning("No profiles found. Please create a profile first!")
            return
        
        profile_names = [p['name'] for p in profiles]
        selected_name = st.selectbox("Select Profile", profile_names)
        
        personalized_cost = config.get('payment', {}).get('pricing', {}).get('financial_astrology', {}).get('personalized_report', 100)
        
        if st.button("📊 Get Personalized Report (₹100)", type="primary"):
            if payment_enabled and current_credits < personalized_cost:
                st.error(f"Insufficient credits! You need {personalized_cost} credits.")
                return
            
            with st.spinner("Generating personalized investment report..."):
                try:
                    profile = next((p for p in profiles if p['name'] == selected_name), None)
                    
                    from src.astrology_engine.vedic_calculator import VedicCalculator
                    calculator = VedicCalculator()
                    chart_data = calculator.calculate_birth_chart(
                        profile['birth_date'],
                        profile['birth_time'],
                        profile['latitude'],
                        profile['longitude']
                    )
                    
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
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
```

### Step 6: Update Buy Credits Page

Add premium credit packs to the existing `show_buy_credits()` function (around line 2607):

```python
# Add after existing bulk packs section:
st.markdown("---")
st.markdown("### 💎 Premium Credits - Financial Astrology")
st.info("Premium features for stock market and investment predictions")

premium_packs = config.get('payment', {}).get('pricing', {}).get('financial_astrology', {}).get('premium_packs', [])

if premium_packs:
    cols = st.columns(len(premium_packs))
    for idx, pack in enumerate(premium_packs):
        with cols[idx]:
            st.markdown(f"""
            <div style='border: 2px solid #FFD700; border-radius: 10px; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;'>
                <h3 style='text-align: center; color: #FFD700;'>{pack['queries']} Financial Queries</h3>
                <h2 style='text-align: center;'>₹{pack['price']}</h2>
                <p style='text-align: center;'>₹{pack['price']//pack['queries']} per query</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Buy {pack['queries']} Premium", key=f"premium_{idx}"):
                st.session_state.selected_pack = pack
                st.session_state.pack_type = 'premium'
```

---

## 📊 Usage Summary

### Career Guidance
- **Cost**: ₹10 (same as standard question)
- **Credits**: Uses standard credit balance
- **Output**: 
  - Top 5 recommended business sectors
  - Planetary strength analysis
  - Sector-specific advice
  - Key astrological factors

### Financial Astrology
- **Market Outlook**: ₹50 per query
  - Overall market sentiment
  - Top 3 performing sectors
  - 3 sectors to avoid
  - Upcoming astrological events
  
- **Sector Analysis**: ₹50 per sector
  - Detailed sector predictions
  - Rating (⭐-based)
  - Timing recommendations
  - Major companies
  
- **Personalized Report**: ₹100
  - Combines birth chart + transits
  - Top 5 personalized sector recommendations
  - Investment timing advice
  - Natal + Transit strength scores

---

## 🔧 Testing Checklist

- [ ] Import modules in app.py
- [ ] Test career analysis with sample profile
- [ ] Test financial market outlook
- [ ] Test sector-specific analysis
- [ ] Test personalized financial report
- [ ] Verify credit deduction (standard vs premium)
- [ ] Test navigation between pages
- [ ] Verify translations in Hindi & Marathi
- [ ] Test with payments disabled (testing mode)
- [ ] Test with payments enabled (production)

---

## 🚀 Deployment Notes

1. **SwissEph Path**: Update in `transit_tracker.py` line 31:
   ```python
   swe.set_ephe_path('/path/to/your/ephe')  # Update to your swisseph data path
   ```

2. **Payment Toggle**: Currently `payment.enabled: false` for testing
   - Set to `true` when ready for production

3. **Premium Credits**: Separate from standard credits conceptually, but stored in same user_credits.json
   - Consider adding `premium_credits` field in future for better tracking

4. **API Rate Limits**: No external APIs used - all calculations local via SwissEph

---

## 📈 Revenue Projection

### Standard Features (₹10/query)
- Career Guidance: ₹10 per analysis
- Regular Questions: ₹10 per query
- Remedies: ₹10 per consultation

### Premium Features (₹50-₹100)
- Market Outlook: ₹50
- Sector Analysis: ₹50
- Personalized Report: ₹100

**Example User Journey**:
- Profile creation: Free
- Birth chart: Free
- Career guidance: ₹10
- Financial market outlook: ₹50
- Personalized investment report: ₹100
- **Total**: ₹160 per comprehensive session

**Bulk Purchase Incentive**:
- 10 standard questions: ₹80 (save ₹20)
- 10 financial queries: ₹350 (save ₹150)
- **Total for serious user**: ₹430 vs ₹600 (save ₹170)

---

## ✅ Next Immediate Steps

1. Run `pip install swisseph` if not already installed
2. Copy the page functions to app.py (after line 2900)
3. Add navigation items (line ~500)
4. Add page routing (line ~540)
5. Add translations for Hindi & Marathi
6. Test with `payment.enabled: false`
7. Restart Streamlit: `streamlit run app.py --server.port 8509`
8. Test all features
9. Enable payments when ready
10. Monitor user feedback and iterate

