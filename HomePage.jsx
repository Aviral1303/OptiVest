import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useInView } from "react-intersection-observer";
import { FaChartLine, FaExchangeAlt, FaShieldAlt, FaCoins, FaTrophy } from "react-icons/fa";

export default function HomePage() {
  const [selectedFeature, setSelectedFeature] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [scrollY, setScrollY] = useState(0);

  // Track mouse position for interactive background
  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("scroll", handleScroll);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  const features = [
    {
      icon: <FaShieldAlt size={40} />,
      title: "Limited Disclosure with Trust Signals",
      description: "Tiered disclosure model with performance badges to build trust without full transparency.",
      details: "Our innovative Semi-Private Disclosure Model offers tiered access to basket information. Free users see asset classes and percentage allocations, while paid subscribers gain insights into detailed components. We build trust through performance badges (low-risk, high-growth, etc.) based on verified historical performance, allowing investors to follow successful traders without requiring complete transparency. This creates an additional revenue stream through premium subscriptions while protecting creators' strategies."
    },
    {
      icon: <FaExchangeAlt size={40} />,
      title: "Multi-Asset Class Flexibility",
      description: "Combine stocks, ETFs, crypto, commodities, REITs, bonds, and alternative assets in one basket.",
      details: "Create diversified investment baskets that break traditional portfolio boundaries. Mix and match across asset classes to build truly personalized investment strategies. Whether you're looking for stability with bonds and blue-chip stocks, or seeking growth with emerging market ETFs and carefully selected cryptocurrencies, our platform gives you unprecedented flexibility to design baskets that match your investment philosophy and goals."
    },
    {
      icon: <FaChartLine size={40} />,
      title: "Dynamic Risk Controls",
      description: "Set risk caps and stop-loss alerts for personalized risk management.",
      details: "Take control of your investment risk with our advanced risk management tools. Set personalized 'risk caps' to limit exposure to specific asset classes (e.g., max 20% in crypto) within any basket you invest in. Our platform automatically implements stop-loss features and sends real-time alerts if a basket's risk metrics exceed your defined thresholds. This appeals particularly to cautious investors who want the benefits of diversification with guardrails against excessive risk."
    },
    {
      icon: <FaCoins size={40} />,
      title: "Creator Incentive Model",
      description: "Earn base earnings, performance bonuses, and referral commissions.",
      details: "Our three-tiered earnings model rewards basket creators generously. Earn Base Earnings as a percentage of returns from investors using your basket. Unlock Performance Bonuses when your baskets outperform market benchmarks. Generate Referral Commissions by bringing new users to the platform. This comprehensive incentive structure encourages creators to develop high-performing baskets, maintain active engagement, and help grow our community."
    },
    {
      icon: <FaTrophy size={40} />,
      title: "Gamification and Social Features",
      description: "Leaderboards, challenges, and social engagement to enhance user retention.",
      details: "Investing meets social competition with our engaging gamification elements. Climb our dynamic leaderboards ranked by returns, risk management, and basket popularity. Participate in time-limited 'Challenges' where you design baskets for specific goals like '10% growth in 6 months' - winners share in platform fee pools. Connect with other investors through comments, endorsements, and earn performance-based badges that showcase your investing expertise. These social elements keep users engaged and create a vibrant investment community."
    }
  ];

  const handleLearnMore = (feature) => {
    setSelectedFeature(feature);
    setShowModal(true);
  };

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: "spring",
        stiffness: 100
      }
    }
  };

  const buttonVariants = {
    hover: {
      scale: 1.05,
      boxShadow: "0px 8px 15px rgba(0, 0, 0, 0.1)",
      transition: {
        type: "spring",
        stiffness: 400,
        damping: 10
      }
    },
    tap: {
      scale: 0.95
    }
  };

  // Interactive background gradient based on mouse position
  const gradientStyle = {
    background: `radial-gradient(circle at ${mousePosition.x}px ${mousePosition.y}px, rgba(59, 130, 246, 0.3) 0%, rgba(16, 185, 129, 0.1) 50%, rgba(30, 58, 138, 0.05) 100%)`,
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    zIndex: -1,
    pointerEvents: "none"
  };

  // Floating elements
  const floatingElements = Array(10).fill().map((_, i) => {
    const size = Math.random() * 50 + 10;
    const initialX = Math.random() * 100;
    const initialY = Math.random() * 100;
    const duration = Math.random() * 20 + 10;
    const delay = Math.random() * 5;

    return (
      <motion.div
        key={i}
        style={{
          position: "fixed",
          width: size,
          height: size,
          borderRadius: "50%",
          background: `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.1)`,
          top: `${initialY}%`,
          left: `${initialX}%`,
          zIndex: -1,
          pointerEvents: "none"
        }}
        animate={{
          y: [0, -50, 0],
          x: [0, 30, 0],
        }}
        transition={{
          duration,
          repeat: Infinity,
          delay,
          ease: "easeInOut"
        }}
      />
    );
  });

  // Parallax effect for header
  const headerParallax = {
    y: scrollY * 0.3
  };

  return (
    <div style={{ 
      minHeight: "100vh", 
      padding: "24px", 
      background: "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
      position: "relative",
      overflow: "hidden"
    }}>
      {/* Interactive background */}
      <div style={gradientStyle} />
      
      {/* Floating elements */}
      {floatingElements}

      <div style={{ maxWidth: "1200px", margin: "0 auto", position: "relative", zIndex: 1 }}>
        {/* Header with parallax effect */}
        <motion.div 
          style={{ 
            textAlign: "center", 
            marginBottom: "80px",
            marginTop: "40px",
            position: "relative"
          }}
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <motion.h1 
            style={{ 
              color: "#1E3A8A", 
              marginBottom: "24px", 
              fontSize: "3.5rem",
              fontWeight: "800",
              background: "linear-gradient(to right, #1E3A8A, #3B82F6)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              textShadow: "0 4px 12px rgba(30, 58, 138, 0.1)"
            }}
            animate={headerParallax}
          >
            Invest Smarter with Multi-Asset Baskets
          </motion.h1>
          
          <motion.p 
            style={{ 
              color: "#4B5563", 
              fontSize: "1.3rem", 
              maxWidth: "800px", 
              margin: "0 auto 48px",
              lineHeight: "1.6"
            }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
          >
            Create, share, and invest in diversified asset baskets. Combine stocks, ETFs, crypto, and more in one place. 
            Build your own investment baskets and earn when others follow your strategy.
          </motion.p>
          
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5, duration: 0.5 }}
          >
            <motion.button 
              style={{ 
                backgroundColor: "#1E3A8A", 
                color: "#fff", 
                padding: "16px 40px", 
                borderRadius: "50px",
                border: "none",
                fontSize: "1.2rem",
                fontWeight: "600",
                cursor: "pointer",
                boxShadow: "0 4px 14px rgba(30, 58, 138, 0.4)",
                marginBottom: "40px"
              }}
              variants={buttonVariants}
              whileHover="hover"
              whileTap="tap"
            >
              Start Investing Now
            </motion.button>
          </motion.div>
        </motion.div>
        
        {/* Features section with animations */}
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          style={{ 
            display: "grid", 
            gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", 
            gap: "30px",
            marginBottom: "80px"
          }}
        >
          {features.map((feature, index) => {
            // Use intersection observer for each feature card
            const [ref, inView] = useInView({
              threshold: 0.2,
              triggerOnce: true
            });
            
            return (
              <motion.div 
                ref={ref}
                key={index} 
                variants={itemVariants}
                style={{ 
                  boxShadow: "0 10px 30px rgba(0,0,0,0.08)", 
                  padding: "30px", 
                  borderRadius: "16px", 
                  backgroundColor: "rgba(255, 255, 255, 0.9)",
                  backdropFilter: "blur(10px)",
                  height: "100%",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "space-between",
                  border: "1px solid rgba(255, 255, 255, 0.2)",
                  transform: inView ? "translateY(0)" : "translateY(50px)",
                  opacity: inView ? 1 : 0,
                  transition: "all 0.6s cubic-bezier(0.17, 0.55, 0.55, 1) " + index * 0.1 + "s"
                }}
                whileHover={{ 
                  y: -10, 
                  boxShadow: "0 20px 40px rgba(0,0,0,0.12)",
                  backgroundColor: "rgba(255, 255, 255, 1)"
                }}
              >
                <div>
                  <div style={{ 
                    color: "#3B82F6", 
                    marginBottom: "20px",
                    display: "inline-block",
                    padding: "16px",
                    borderRadius: "12px",
                    background: "rgba(59, 130, 246, 0.1)"
                  }}>
                    {feature.icon}
                  </div>
                  <h2 style={{ 
                    color: "#1E3A8A", 
                    marginBottom: "16px",
                    fontSize: "1.5rem",
                    fontWeight: "700"
                  }}>
                    {feature.title}
                  </h2>
                  <p style={{ 
                    color: "#4B5563", 
                    marginBottom: "24px",
                    lineHeight: "1.6"
                  }}>
                    {feature.description}
                  </p>
                </div>
                <motion.button 
                  style={{ 
                    marginTop: "16px", 
                    backgroundColor: "#3B82F6", 
                    color: "#fff", 
                    padding: "12px 24px", 
                    borderRadius: "8px",
                    border: "none",
                    cursor: "pointer",
                    fontWeight: "600",
                    boxShadow: "0 4px 6px rgba(59, 130, 246, 0.3)"
                  }} 
                  variants={buttonVariants}
                  whileHover="hover"
                  whileTap="tap"
                  onClick={() => handleLearnMore(feature)}
                >
                  Learn More
                </motion.button>
              </motion.div>
            );
          })}
        </motion.div>
        
        {/* Call to action section */}
        <motion.div 
          style={{ 
            textAlign: "center", 
            marginTop: "80px",
            marginBottom: "60px",
            padding: "60px 40px",
            borderRadius: "24px",
            background: "linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%)",
            boxShadow: "0 20px 40px rgba(30, 58, 138, 0.3)"
          }}
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <h2 style={{ 
            color: "#fff", 
            marginBottom: "24px",
            fontSize: "2.2rem",
            fontWeight: "700"
          }}>
            Ready to revolutionize your investment strategy?
          </h2>
          <p style={{ 
            color: "rgba(255, 255, 255, 0.9)", 
            marginBottom: "32px",
            fontSize: "1.2rem",
            maxWidth: "700px",
            margin: "0 auto 32px"
          }}>
            Join thousands of investors creating and sharing multi-asset baskets.
          </p>
          <motion.button 
            style={{ 
              backgroundColor: "#fff", 
              color: "#1E3A8A", 
              padding: "16px 40px", 
              borderRadius: "50px",
              border: "none",
              fontSize: "1.2rem",
              fontWeight: "700",
              cursor: "pointer",
              boxShadow: "0 4px 14px rgba(0, 0, 0, 0.2)"
            }}
            variants={buttonVariants}
            whileHover="hover"
            whileTap="tap"
          >
            Get Started Now
          </motion.button>
        </motion.div>
      </div>

      {/* Animated modal */}
      <AnimatePresence>
        {showModal && (
          <motion.div 
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
              padding: "20px",
              backdropFilter: "blur(8px)"
            }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setShowModal(false)}
          >
            <motion.div 
              style={{ 
                backgroundColor: "#fff", 
                padding: "40px", 
                borderRadius: "20px", 
                boxShadow: "0 25px 50px rgba(0,0,0,0.3)",
                maxWidth: "700px",
                width: "100%",
                position: "relative",
                overflow: "hidden"
              }}
              initial={{ scale: 0.8, y: 50, opacity: 0 }}
              animate={{ scale: 1, y: 0, opacity: 1 }}
              exit={{ scale: 0.8, y: 50, opacity: 0 }}
              transition={{ type: "spring", damping: 25 }}
              onClick={(e) => e.stopPropagation()}
            >
              <div style={{ 
                position: "absolute", 
                top: 0, 
                left: 0, 
                right: 0, 
                height: "8px", 
                background: "linear-gradient(to right, #3B82F6, #10B981)" 
              }} />
              
              <div style={{ marginBottom: "24px" }}>
                <div style={{ 
                  color: "#3B82F6", 
                  marginBottom: "20px",
                  display: "inline-block",
                  padding: "16px",
                  borderRadius: "12px",
                  background: "rgba(59, 130, 246, 0.1)"
                }}>
                  {selectedFeature?.icon}
                </div>
              </div>
              
              <h3 style={{ 
                color: "#1E3A8A", 
                fontSize: "1.8rem", 
                marginBottom: "20px",
                fontWeight: "700"
              }}>
                {selectedFeature?.title}
              </h3>
              
              <p style={{ 
                color: "#1F2937", 
                fontWeight: "600", 
                marginBottom: "20px",
                fontSize: "1.1rem"
              }}>
                {selectedFeature?.description}
              </p>
              
              <p style={{ 
                color: "#4B5563", 
                lineHeight: "1.8", 
                marginBottom: "30px",
                fontSize: "1rem"
              }}>
                {selectedFeature?.details}
              </p>
              
              <div style={{ 
                display: "flex", 
                justifyContent: "space-between",
                marginTop: "30px"
              }}>
                <motion.button 
                  style={{ 
                    backgroundColor: "#E5E7EB", 
                    color: "#1F2937", 
                    padding: "12px 28px", 
                    borderRadius: "8px",
                    border: "none",
                    fontWeight: "600",
                    cursor: "pointer"
                  }} 
                  variants={buttonVariants}
                  whileHover="hover"
                  whileTap="tap"
                  onClick={() => setShowModal(false)}
                >
                  Close
                </motion.button>
                
                <motion.button 
                  style={{ 
                    backgroundColor: "#10B981", 
                    color: "#fff", 
                    padding: "12px 28px", 
                    borderRadius: "8px",
                    border: "none",
                    fontWeight: "600",
                    cursor: "pointer",
                    boxShadow: "0 4px 6px rgba(16, 185, 129, 0.3)"
                  }}
                  variants={buttonVariants}
                  whileHover="hover"
                  whileTap="tap"
                >
                  Try This Feature
                </motion.button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
} 