# PASTE THIS AT THE END OF app.py (before if __name__ == "__main__":)
# Career Guidance & Financial Astrology Pages

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
