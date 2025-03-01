import React, { useState } from "react";

export default function HomePage() {
  const [selectedFeature, setSelectedFeature] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const features = [
    {
      title: "Limited Disclosure with Trust Signals",
      description: "Tiered disclosure model with performance badges to build trust without full transparency.",
      details: "Our innovative Semi-Private Disclosure Model offers tiered access to basket information. Free users see asset classes and percentage allocations, while paid subscribers gain insights into detailed components. We build trust through performance badges (low-risk, high-growth, etc.) based on verified historical performance, allowing investors to follow successful traders without requiring complete transparency. This creates an additional revenue stream through premium subscriptions while protecting creators' strategies."
    },
    {
      title: "Multi-Asset Class Flexibility",
      description: "Combine stocks, ETFs, crypto, commodities, REITs, bonds, and alternative assets in one basket.",
      details: "Create diversified investment baskets that break traditional portfolio boundaries. Mix and match across asset classes to build truly personalized investment strategies. Whether you're looking for stability with bonds and blue-chip stocks, or seeking growth with emerging market ETFs and carefully selected cryptocurrencies, our platform gives you unprecedented flexibility to design baskets that match your investment philosophy and goals."
    },
    {
      title: "Dynamic Risk Controls",
      description: "Set risk caps and stop-loss alerts for personalized risk management.",
      details: "Take control of your investment risk with our advanced risk management tools. Set personalized 'risk caps' to limit exposure to specific asset classes (e.g., max 20% in crypto) within any basket you invest in. Our platform automatically implements stop-loss features and sends real-time alerts if a basket's risk metrics exceed your defined thresholds. This appeals particularly to cautious investors who want the benefits of diversification with guardrails against excessive risk."
    },
    {
      title: "Creator Incentive Model",
      description: "Earn base earnings, performance bonuses, and referral commissions.",
      details: "Our three-tiered earnings model rewards basket creators generously. Earn Base Earnings as a percentage of returns from investors using your basket. Unlock Performance Bonuses when your baskets outperform market benchmarks. Generate Referral Commissions by bringing new users to the platform. This comprehensive incentive structure encourages creators to develop high-performing baskets, maintain active engagement, and help grow our community."
    },
    {
      title: "Gamification and Social Features",
      description: "Leaderboards, challenges, and social engagement to enhance user retention.",
      details: "Investing meets social competition with our engaging gamification elements. Climb our dynamic leaderboards ranked by returns, risk management, and basket popularity. Participate in time-limited 'Challenges' where you design baskets for specific goals like '10% growth in 6 months' - winners share in platform fee pools. Connect with other investors through comments, endorsements, and earn performance-based badges that showcase your investing expertise. These social elements keep users engaged and create a vibrant investment community."
    }
  ];

  const handleLearnMore = (feature) => {
    setSelectedFeature(feature);
    setShowModal(true);
  };

  return (
    <div style={{ minHeight: "100vh", padding: "24px", background: "linear-gradient(to bottom, #ebf8ff, #fff)" }}>
      <div style={{ maxWidth: "1200px", margin: "0 auto" }}>
        <h1 style={{ textAlign: "center", color: "#1E3A8A", marginBottom: "24px", fontSize: "2.5rem" }}>Invest Smarter with Multi-Asset Baskets</h1>
        <p style={{ textAlign: "center", color: "#4B5563", marginBottom: "48px", fontSize: "1.2rem", maxWidth: "800px", margin: "0 auto 48px" }}>
          Create, share, and invest in diversified asset baskets. Combine stocks, ETFs, crypto, and more in one place. 
          Build your own investment baskets and earn when others follow your strategy.
        </p>
        
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: "24px" }}>
          {features.map((feature, index) => (
            <div 
              key={index} 
              style={{ 
                boxShadow: "0 4px 8px rgba(0,0,0,0.1)", 
                padding: "24px", 
                borderRadius: "12px", 
                backgroundColor: "#fff",
                transition: "transform 0.3s ease, box-shadow 0.3s ease",
                height: "100%",
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between"
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = "translateY(-5px)";
                e.currentTarget.style.boxShadow = "0 8px 16px rgba(0,0,0,0.15)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = "translateY(0)";
                e.currentTarget.style.boxShadow = "0 4px 8px rgba(0,0,0,0.1)";
              }}
            >
              <div>
                <h2 style={{ color: "#1E3A8A", marginBottom: "12px" }}>{feature.title}</h2>
                <p style={{ color: "#374151", marginBottom: "16px" }}>{feature.description}</p>
              </div>
              <button 
                style={{ 
                  marginTop: "16px", 
                  backgroundColor: "#1E3A8A", 
                  color: "#fff", 
                  padding: "10px 20px", 
                  borderRadius: "6px",
                  border: "none",
                  cursor: "pointer",
                  fontWeight: "600",
                  transition: "background-color 0.3s ease"
                }} 
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = "#2D4BA0"}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = "#1E3A8A"}
                onClick={() => handleLearnMore(feature)}
              >
                Learn More
              </button>
            </div>
          ))}
        </div>
        
        <div style={{ textAlign: "center", marginTop: "64px" }}>
          <h2 style={{ color: "#1E3A8A", marginBottom: "16px" }}>Ready to revolutionize your investment strategy?</h2>
          <p style={{ color: "#4B5563", marginBottom: "24px" }}>Join thousands of investors creating and sharing multi-asset baskets.</p>
          <button 
            style={{ 
              backgroundColor: "#1E3A8A", 
              color: "#fff", 
              padding: "12px 32px", 
              borderRadius: "8px",
              border: "none",
              fontSize: "1.1rem",
              fontWeight: "600",
              cursor: "pointer",
              transition: "background-color 0.3s ease"
            }}
            onMouseEnter={(e) => e.currentTarget.style.backgroundColor = "#2D4BA0"}
            onMouseLeave={(e) => e.currentTarget.style.backgroundColor = "#1E3A8A"}
          >
            Get Started Now
          </button>
        </div>
      </div>

      {showModal && (
        <div 
          style={{ 
            position: "fixed", 
            top: 0, 
            left: 0, 
            right: 0, 
            bottom: 0, 
            backgroundColor: "rgba(0,0,0,0.7)", 
            display: "flex", 
            alignItems: "center", 
            justifyContent: "center",
            zIndex: 1000,
            padding: "20px"
          }}
          onClick={() => setShowModal(false)}
        >
          <div 
            style={{ 
              backgroundColor: "#fff", 
              padding: "32px", 
              borderRadius: "12px", 
              boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
              maxWidth: "600px",
              width: "100%"
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <h3 style={{ color: "#1E3A8A", fontSize: "1.5rem", marginBottom: "16px" }}>{selectedFeature.title}</h3>
            <p style={{ color: "#1F2937", fontWeight: "600", marginBottom: "16px" }}>{selectedFeature.description}</p>
            <p style={{ color: "#4B5563", lineHeight: "1.6", marginBottom: "24px" }}>{selectedFeature.details}</p>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <button 
                style={{ 
                  backgroundColor: "#1E3A8A", 
                  color: "#fff", 
                  padding: "10px 24px", 
                  borderRadius: "6px",
                  border: "none",
                  fontWeight: "600",
                  cursor: "pointer"
                }} 
                onClick={() => setShowModal(false)}
              >
                Close
              </button>
              <button 
                style={{ 
                  backgroundColor: "#10B981", 
                  color: "#fff", 
                  padding: "10px 24px", 
                  borderRadius: "6px",
                  border: "none",
                  fontWeight: "600",
                  cursor: "pointer"
                }}
              >
                Try This Feature
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 