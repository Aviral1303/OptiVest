import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence, useAnimation } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { 
  FaLock, 
  FaChartLine, 
  FaShieldAlt, 
  FaChartBar, 
  FaRegChartBar, 
  FaLightbulb, 
  FaExchangeAlt, 
  FaBalanceScale,
  FaDatabase,
  FaProjectDiagram,
  FaRobot
} from 'react-icons/fa';

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
      title: "Limited Disclosure with Trust Signals",
      description: "Maintain privacy while building trust with counterparties through selective disclosure.",
      details: "Our platform allows you to share only the necessary information about your portfolio while still providing sufficient trust signals to counterparties. This selective disclosure mechanism protects your proprietary strategies while enabling efficient transactions.",
      icon: <FaLock size={30} />
    },
    {
      title: "Multi-Asset Class Flexibility",
      description: "Seamlessly integrate stocks, ETFs, crypto, commodities, and more in one unified platform.",
      details: "OptiVest's advanced multi-asset framework allows you to build truly diversified portfolios across traditional and alternative asset classes. Our platform handles the complexities of different market structures, trading hours, and data formats to provide a unified view of your investments.",
      icon: <FaExchangeAlt size={30} />
    },
    {
      title: "Dynamic Risk Controls",
      description: "Implement sophisticated risk management with real-time monitoring and automated safeguards.",
      details: "Our platform continuously monitors your portfolio for risk exposures across multiple dimensions including volatility, correlation shifts, liquidity constraints, and tail events. Automated circuit breakers can be configured to protect your investments during market turbulence.",
      icon: <FaShieldAlt size={30} />
    },
    {
      title: "Advanced Portfolio Analytics",
      description: "Gain deeper insights with institutional-grade analytics that reveal hidden risks and opportunities.",
      details: "Access sophisticated analytics typically available only to institutional investors. Our platform provides factor analysis, stress testing, scenario modeling, and performance attribution to help you understand the true drivers of your portfolio's performance and risk.",
      icon: <FaChartLine size={30} />
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
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5
      }
    }
  };

  const buttonVariants = {
    hover: { 
      scale: 1.05, 
      boxShadow: "0 10px 20px rgba(0, 0, 0, 0.3)",
      transition: { duration: 0.3 }
    },
    tap: { scale: 0.95 }
  };

  // Interactive background gradient based on mouse position
  const gradientStyle = {
    background: `radial-gradient(circle at ${mousePosition.x}px ${mousePosition.y}px, rgba(23, 37, 84, 0.7) 0%, rgba(220, 38, 38, 0.2) 50%, rgba(30, 58, 138, 0.1) 100%)`,
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    zIndex: -1,
    pointerEvents: "none"
  };

  // Floating elements
  const floatingElements = Array(15).fill().map((_, i) => {
    const size = Math.random() * 60 + 10;
    const initialX = Math.random() * 100;
    const initialY = Math.random() * 100;
    const duration = Math.random() * 20 + 10;
    const delay = Math.random() * 5;
    
    // Use our color scheme
    const colors = [
      "rgba(23, 37, 84, 0.1)",  // Dark blue
      "rgba(30, 58, 138, 0.1)",  // Blue
      "rgba(220, 38, 38, 0.1)",  // Red
      "rgba(185, 28, 28, 0.1)",  // Dark red
      "rgba(0, 0, 0, 0.05)"      // Black
    ];
    
    const color = colors[Math.floor(Math.random() * colors.length)];

    return (
      <motion.div
        key={i}
        style={{
          position: "fixed",
          width: size,
          height: size,
          borderRadius: "50%",
          background: color,
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

  // Stock chart visualization
  const StockChart = () => {
    return (
      <motion.div
        style={{
          position: "absolute",
          right: "-5%",
          top: "20%",
          width: "300px",
          height: "200px",
          opacity: 0.2,
          zIndex: 0
        }}
        initial={{ opacity: 0, x: 50 }}
        animate={{ opacity: 0.2, x: 0 }}
        transition={{ duration: 1, delay: 1 }}
      >
        <svg width="300" height="200" viewBox="0 0 300 200">
          <path
            d="M0,150 C20,130 40,180 60,120 C80,100 100,110 120,80 C140,60 160,90 180,40 C200,20 220,50 240,30 C260,40 280,10 300,30"
            fill="none"
            stroke="#DC2626"
            strokeWidth="3"
          />
          <path
            d="M0,170 C20,160 40,150 60,140 C80,160 100,130 120,120 C140,110 160,140 180,100 C200,90 220,110 240,80 C260,70 280,60 300,50"
            fill="none"
            stroke="#1E3A8A"
            strokeWidth="3"
          />
        </svg>
      </motion.div>
    );
  };

  // Financial data visualization
  const DataVisualization = () => {
    return (
      <motion.div
        style={{
          position: "absolute",
          left: "-5%",
          bottom: "15%",
          width: "250px",
          height: "250px",
          opacity: 0.15,
          zIndex: 0
        }}
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 0.15, x: 0 }}
        transition={{ duration: 1, delay: 1.5 }}
      >
        <svg width="250" height="250" viewBox="0 0 250 250">
          <rect x="10" y="50" width="30" height="150" fill="#1E3A8A" />
          <rect x="50" y="80" width="30" height="120" fill="#DC2626" />
          <rect x="90" y="100" width="30" height="100" fill="#1E3A8A" />
          <rect x="130" y="60" width="30" height="140" fill="#DC2626" />
          <rect x="170" y="90" width="30" height="110" fill="#1E3A8A" />
          <rect x="210" y="40" width="30" height="160" fill="#DC2626" />
        </svg>
      </motion.div>
    );
  };

  // Parallax effect for header
  const headerParallax = {
    x: mousePosition.x / 100,
    y: mousePosition.y / 100
  };

  return (
    <div style={{ 
      minHeight: "100vh", 
      padding: "24px", 
      background: "#000000",
      position: "relative",
      overflow: "hidden",
      color: "#ffffff"
    }}>
      {/* Interactive background */}
      <div style={gradientStyle} />
      
      {/* Floating elements */}
      {floatingElements}

      <div style={{ maxWidth: "1200px", margin: "0 auto", position: "relative", zIndex: 1 }}>
        {/* Visual elements */}
        <StockChart />
        <DataVisualization />
        
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
              marginBottom: "24px", 
              fontSize: "3.8rem",
              fontWeight: "800",
              background: "linear-gradient(to right, #DC2626, #1E3A8A)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              textShadow: "0 4px 12px rgba(220, 38, 38, 0.3)"
            }}
            animate={headerParallax}
          >
            Optimize Your Portfolio with Multi-Asset Baskets
          </motion.h1>
          
          <motion.p 
            style={{ 
              color: "#f1f1f1", 
              fontSize: "1.3rem", 
              maxWidth: "800px", 
              margin: "0 auto 48px",
              lineHeight: "1.6"
            }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
          >
            Discover the power of true diversification with OptiVest's multi-asset investment platform. 
            Combine stocks, ETFs, crypto, commodities, and more in one place for optimized risk-adjusted returns.
          </motion.p>
          
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5, duration: 0.5 }}
          >
            <motion.button 
              style={{ 
                backgroundColor: "#DC2626", 
                color: "#fff", 
                padding: "16px 40px", 
                borderRadius: "50px",
                border: "none",
                fontSize: "1.2rem",
                fontWeight: "600",
                cursor: "pointer",
                boxShadow: "0 4px 14px rgba(220, 38, 38, 0.4)",
                marginBottom: "40px"
              }}
              variants={buttonVariants}
              whileHover="hover"
              whileTap="tap"
            >
              Start Investing Now
            </motion.button>
          </motion.div>
          
          {/* Enhanced Visual indicator for multi-asset capabilities */}
          <motion.div
            style={{
              display: "flex",
              justifyContent: "center",
              gap: "20px",
              marginBottom: "30px",
              flexWrap: "wrap"
            }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8, duration: 0.5 }}
          >
            <motion.div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                backgroundColor: "rgba(30, 58, 138, 0.2)",
                padding: "8px 16px",
                borderRadius: "50px"
              }}
              whileHover={{ scale: 1.05 }}
            >
              <FaChartBar size={20} color="#DC2626" />
              <span style={{ color: "#f1f1f1" }}>Optimized Returns</span>
            </motion.div>
            <motion.div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                backgroundColor: "rgba(220, 38, 38, 0.2)",
                padding: "8px 16px",
                borderRadius: "50px"
              }}
              whileHover={{ scale: 1.05 }}
            >
              <FaRegChartBar size={20} color="#1E3A8A" />
              <span style={{ color: "#f1f1f1" }}>Reduced Volatility</span>
            </motion.div>
            <motion.div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                backgroundColor: "rgba(4, 120, 87, 0.2)",
                padding: "8px 16px",
                borderRadius: "50px"
              }}
              whileHover={{ scale: 1.05 }}
            >
              <FaLightbulb size={20} color="#F59E0B" />
              <span style={{ color: "#f1f1f1" }}>Advanced Analytics</span>
            </motion.div>
            <motion.div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                backgroundColor: "rgba(147, 51, 234, 0.2)",
                padding: "8px 16px",
                borderRadius: "50px"
              }}
              whileHover={{ scale: 1.05 }}
            >
              <FaExchangeAlt size={20} color="#047857" />
              <span style={{ color: "#f1f1f1" }}>Multi-Asset Diversification</span>
            </motion.div>
            <motion.div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                backgroundColor: "rgba(236, 72, 153, 0.2)",
                padding: "8px 16px",
                borderRadius: "50px"
              }}
              whileHover={{ scale: 1.05 }}
            >
              <FaBalanceScale size={20} color="#EC4899" />
              <span style={{ color: "#f1f1f1" }}>Risk-Adjusted Performance</span>
            </motion.div>
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
                  boxShadow: "0 10px 30px rgba(0,0,0,0.3)", 
                  padding: "30px", 
                  borderRadius: "16px", 
                  backgroundColor: "rgba(17, 24, 39, 0.8)",
                  backdropFilter: "blur(10px)",
                  height: "100%",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "space-between",
                  border: "1px solid rgba(30, 58, 138, 0.2)",
                  transform: inView ? "translateY(0)" : "translateY(50px)",
                  opacity: inView ? 1 : 0,
                  transition: "all 0.6s cubic-bezier(0.17, 0.55, 0.55, 1) " + index * 0.1 + "s"
                }}
                whileHover={{ 
                  y: -10, 
                  boxShadow: "0 20px 40px rgba(220, 38, 38, 0.2)",
                  backgroundColor: "rgba(17, 24, 39, 0.95)"
                }}
              >
                <div>
                  <div style={{ 
                    color: index % 2 === 0 ? "#DC2626" : "#1E3A8A", 
                    marginBottom: "20px",
                    display: "inline-block",
                    padding: "16px",
                    borderRadius: "12px",
                    background: index % 2 === 0 ? "rgba(220, 38, 38, 0.1)" : "rgba(30, 58, 138, 0.1)"
                  }}>
                    {feature.icon}
                  </div>
                  <h2 style={{ 
                    color: "#ffffff", 
                    marginBottom: "16px",
                    fontSize: "1.5rem",
                    fontWeight: "700"
                  }}>
                    {feature.title}
                  </h2>
                  <p style={{ 
                    color: "#d1d5db", 
                    marginBottom: "24px",
                    lineHeight: "1.6"
                  }}>
                    {feature.description}
                  </p>
                </div>
                <motion.button 
                  style={{ 
                    marginTop: "16px", 
                    backgroundColor: index % 2 === 0 ? "#DC2626" : "#1E3A8A", 
                    color: "#fff", 
                    padding: "12px 24px", 
                    borderRadius: "8px",
                    border: "none",
                    cursor: "pointer",
                    fontWeight: "600",
                    boxShadow: index % 2 === 0 
                      ? "0 4px 6px rgba(220, 38, 38, 0.3)" 
                      : "0 4px 6px rgba(30, 58, 138, 0.3)"
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
        
        {/* Interactive Portfolio Visualization - Enhanced for multi-asset */}
        <motion.div
          style={{
            marginTop: "60px",
            marginBottom: "80px",
            padding: "40px",
            borderRadius: "20px",
            backgroundColor: "rgba(17, 24, 39, 0.7)",
            backdropFilter: "blur(10px)",
            boxShadow: "0 20px 40px rgba(0, 0, 0, 0.4)",
            border: "1px solid rgba(30, 58, 138, 0.2)"
          }}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h2 style={{
            textAlign: "center",
            fontSize: "2rem",
            fontWeight: "700",
            marginBottom: "40px",
            color: "#ffffff"
          }}>
            Advanced Multi-Asset Portfolio Visualization
          </h2>
          
          <div style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "30px"
          }}>
            <div style={{
              display: "flex",
              flexWrap: "wrap",
              justifyContent: "center",
              gap: "20px",
              marginBottom: "30px"
            }}>
              {/* Asset Class Allocation Visualization - Enhanced with more asset classes */}
              <motion.div
                style={{
                  width: "300px",
                  height: "300px",
                  position: "relative",
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center"
                }}
                whileHover={{ scale: 1.05 }}
              >
                <svg width="300" height="300" viewBox="0 0 300 300">
                  {/* Donut chart segments - Updated with more asset classes */}
                  <circle cx="150" cy="150" r="100" fill="none" stroke="#1E3A8A" strokeWidth="40" strokeDasharray="125 628" strokeDashoffset="0" />
                  <circle cx="150" cy="150" r="100" fill="none" stroke="#DC2626" strokeWidth="40" strokeDasharray="94 628" strokeDashoffset="125" />
                  <circle cx="150" cy="150" r="100" fill="none" stroke="#047857" strokeWidth="40" strokeDasharray="78 628" strokeDashoffset="219" />
                  <circle cx="150" cy="150" r="100" fill="none" stroke="#9333EA" strokeWidth="40" strokeDasharray="63 628" strokeDashoffset="297" />
                  <circle cx="150" cy="150" r="100" fill="none" stroke="#F59E0B" strokeWidth="40" strokeDasharray="47 628" strokeDashoffset="360" />
                  <circle cx="150" cy="150" r="100" fill="none" stroke="#EC4899" strokeWidth="40" strokeDasharray="31 628" strokeDashoffset="407" />
                  <circle cx="150" cy="150" r="100" fill="none" stroke="#0EA5E9" strokeWidth="40" strokeDasharray="31 628" strokeDashoffset="438" />
                  <circle cx="150" cy="150" r="100" fill="none" stroke="#84CC16" strokeWidth="40" strokeDasharray="31 628" strokeDashoffset="469" />
                  
                  {/* Center circle */}
                  <circle cx="150" cy="150" r="60" fill="#111827" />
                  <text x="150" y="150" textAnchor="middle" dominantBaseline="middle" fill="#ffffff" fontSize="14" fontWeight="600">Asset Allocation</text>
                </svg>
                
                {/* Legend - Updated with more asset classes */}
                <div style={{
                  position: "absolute",
                  bottom: "-120px",
                  left: "0",
                  right: "0",
                  display: "flex",
                  flexWrap: "wrap",
                  justifyContent: "center",
                  gap: "10px"
                }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                    <div style={{ width: "12px", height: "12px", backgroundColor: "#1E3A8A", borderRadius: "2px" }}></div>
                    <span style={{ color: "#d1d5db", fontSize: "12px" }}>Stocks (20%)</span>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                    <div style={{ width: "12px", height: "12px", backgroundColor: "#DC2626", borderRadius: "2px" }}></div>
                    <span style={{ color: "#d1d5db", fontSize: "12px" }}>ETFs (15%)</span>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                    <div style={{ width: "12px", height: "12px", backgroundColor: "#047857", borderRadius: "2px" }}></div>
                    <span style={{ color: "#d1d5db", fontSize: "12px" }}>Crypto (12.5%)</span>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                    <div style={{ width: "12px", height: "12px", backgroundColor: "#9333EA", borderRadius: "2px" }}></div>
                    <span style={{ color: "#d1d5db", fontSize: "12px" }}>Bonds (10%)</span>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                    <div style={{ width: "12px", height: "12px", backgroundColor: "#F59E0B", borderRadius: "2px" }}></div>
                    <span style={{ color: "#d1d5db", fontSize: "12px" }}>Commodities (7.5%)</span>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                    <div style={{ width: "12px", height: "12px", backgroundColor: "#EC4899", borderRadius: "2px" }}></div>
                    <span style={{ color: "#d1d5db", fontSize: "12px" }}>Real Estate (5%)</span>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                    <div style={{ width: "12px", height: "12px", backgroundColor: "#0EA5E9", borderRadius: "2px" }}></div>
                    <span style={{ color: "#d1d5db", fontSize: "12px" }}>Forex (5%)</span>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                    <div style={{ width: "12px", height: "12px", backgroundColor: "#84CC16", borderRadius: "2px" }}></div>
                    <span style={{ color: "#d1d5db", fontSize: "12px" }}>Alternatives (5%)</span>
                  </div>
                </div>
              </motion.div>
              
              {/* Risk-Return Visualization */}
              <motion.div
                style={{
                  width: "300px",
                  height: "300px",
                  position: "relative"
                }}
                whileHover={{ scale: 1.05 }}
              >
                <svg width="300" height="300" viewBox="0 0 300 300">
                  {/* Axes */}
                  <line x1="50" y1="250" x2="250" y2="250" stroke="#6B7280" strokeWidth="2" />
                  <line x1="50" y1="50" x2="50" y2="250" stroke="#6B7280" strokeWidth="2" />
                  
                  {/* Axis labels */}
                  <text x="150" y="280" textAnchor="middle" fill="#9CA3AF" fontSize="12">Risk</text>
                  <text x="20" y="150" textAnchor="middle" fill="#9CA3AF" fontSize="12" transform="rotate(-90, 20, 150)">Return</text>
                  
                  {/* Grid lines */}
                  <line x1="50" y1="200" x2="250" y2="200" stroke="#374151" strokeWidth="1" strokeDasharray="5,5" />
                  <line x1="50" y1="150" x2="250" y2="150" stroke="#374151" strokeWidth="1" strokeDasharray="5,5" />
                  <line x1="50" y1="100" x2="250" y2="100" stroke="#374151" strokeWidth="1" strokeDasharray="5,5" />
                  <line x1="100" y1="50" x2="100" y2="250" stroke="#374151" strokeWidth="1" strokeDasharray="5,5" />
                  <line x1="150" y1="50" x2="150" y2="250" stroke="#374151" strokeWidth="1" strokeDasharray="5,5" />
                  <line x1="200" y1="50" x2="200" y2="250" stroke="#374151" strokeWidth="1" strokeDasharray="5,5" />
                  
                  {/* Efficient frontier curve */}
                  <path d="M70,220 Q120,120 230,80" fill="none" stroke="#1E3A8A" strokeWidth="2" strokeDasharray="5,5" />
                  
                  {/* Portfolio points */}
                  <circle cx="90" cy="200" r="8" fill="#DC2626" />
                  <circle cx="130" cy="170" r="8" fill="#047857" />
                  <circle cx="170" cy="130" r="10" fill="#F59E0B" stroke="#ffffff" strokeWidth="2" />
                  <circle cx="210" cy="100" r="8" fill="#9333EA" />
                  
                  {/* Legend */}
                  <text x="150" y="40" textAnchor="middle" fill="#ffffff" fontSize="14" fontWeight="600">Risk-Return Profile</text>
                </svg>
                
                {/* Legend */}
                <div style={{
                  position: "absolute",
                  bottom: "-80px",
                  left: "0",
                  right: "0",
                  display: "flex",
                  flexWrap: "wrap",
                  justifyContent: "center",
                  gap: "10px"
                }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                    <div style={{ width: "12px", height: "12px", backgroundColor: "#DC2626", borderRadius: "50%" }}></div>
                    <span style={{ color: "#d1d5db", fontSize: "12px" }}>Conservative</span>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                    <div style={{ width: "12px", height: "12px", backgroundColor: "#047857", borderRadius: "50%" }}></div>
                    <span style={{ color: "#d1d5db", fontSize: "12px" }}>Balanced</span>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                    <div style={{ width: "12px", height: "12px", backgroundColor: "#F59E0B", borderRadius: "50%" }}></div>
                    <span style={{ color: "#d1d5db", fontSize: "12px" }}>Optimized</span>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                    <div style={{ width: "12px", height: "12px", backgroundColor: "#9333EA", borderRadius: "50%" }}></div>
                    <span style={{ color: "#d1d5db", fontSize: "12px" }}>Aggressive</span>
                  </div>
                </div>
              </motion.div>
            </div>
            
            <motion.p
              style={{
                color: "#d1d5db",
                textAlign: "center",
                maxWidth: "800px",
                margin: "0 auto",
                lineHeight: "1.6"
              }}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5, duration: 0.8 }}
            >
              Our advanced multi-asset portfolio visualization tools help you understand the true composition and performance characteristics of your investments across all asset classes. 
              Optimize your asset allocation for the perfect balance of risk and return based on your investment goals, with support for stocks, ETFs, crypto, commodities, bonds, real estate, forex, and alternative investments.
            </motion.p>
          </div>
        </motion.div>
        
        {/* Call to action section */}
        <motion.div 
          style={{ 
            textAlign: "center", 
            marginTop: "80px",
            marginBottom: "60px",
            padding: "60px 40px",
            borderRadius: "24px",
            background: "linear-gradient(135deg, #000000 0%, #1E3A8A 100%)",
            boxShadow: "0 20px 40px rgba(0, 0, 0, 0.5)",
            border: "1px solid rgba(30, 58, 138, 0.3)"
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
            Ready to optimize your investment portfolio?
          </h2>
          <p style={{ 
            color: "rgba(255, 255, 255, 0.9)", 
            marginBottom: "32px",
            fontSize: "1.2rem",
            maxWidth: "700px",
            margin: "0 auto 32px"
          }}>
            Experience the power of institutional-grade portfolio analytics and true multi-asset diversification.
          </p>
          <motion.button 
            style={{ 
              backgroundColor: "#DC2626", 
              color: "#fff", 
              padding: "16px 40px", 
              borderRadius: "50px",
              border: "none",
              fontSize: "1.2rem",
              fontWeight: "700",
              cursor: "pointer",
              boxShadow: "0 4px 14px rgba(220, 38, 38, 0.4)"
            }}
            variants={buttonVariants}
            whileHover="hover"
            whileTap="tap"
          >
            Start Optimizing Now
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
              backgroundColor: "rgba(0,0,0,0.8)", 
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
                backgroundColor: "#111827", 
                padding: "40px", 
                borderRadius: "20px", 
                boxShadow: "0 25px 50px rgba(0,0,0,0.5)",
                maxWidth: "700px",
                width: "100%",
                position: "relative",
                overflow: "hidden",
                border: "1px solid rgba(30, 58, 138, 0.2)"
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
                background: "linear-gradient(to right, #DC2626, #1E3A8A)" 
              }} />
              
              <div style={{ marginBottom: "24px" }}>
                <div style={{ 
                  color: "#DC2626", 
                  marginBottom: "20px",
                  display: "inline-block",
                  padding: "16px",
                  borderRadius: "12px",
                  background: "rgba(220, 38, 38, 0.1)"
                }}>
                  {selectedFeature?.icon}
                </div>
              </div>
              
              <h3 style={{ 
                color: "#ffffff", 
                fontSize: "1.8rem", 
                marginBottom: "20px",
                fontWeight: "700"
              }}>
                {selectedFeature?.title}
              </h3>
              
              <p style={{ 
                color: "#d1d5db", 
                fontWeight: "600", 
                marginBottom: "20px",
                fontSize: "1.1rem"
              }}>
                {selectedFeature?.description}
              </p>
              
              <p style={{ 
                color: "#9ca3af", 
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
                    backgroundColor: "#374151", 
                    color: "#ffffff", 
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
                    backgroundColor: "#DC2626", 
                    color: "#fff", 
                    padding: "12px 28px", 
                    borderRadius: "8px",
                    border: "none",
                    fontWeight: "600",
                    cursor: "pointer",
                    boxShadow: "0 4px 6px rgba(220, 38, 38, 0.3)"
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