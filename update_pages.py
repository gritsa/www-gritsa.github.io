#!/usr/bin/env python3
import re
import sys

def update_page(page_name):
    file_path = f"{page_name}/index.html"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Standardized header with ../ paths for subpages
    new_header = '''	<div class="preloader">
		<div class="loading-container">
			<div class="loading"></div>
			<div id="loading-icon"><img src="../images/Gritsa-Logo-2026.png" alt=""></div>
		</div>
	</div>
	<!-- Preloader End -->

    <!-- Header Start -->
	<header class="main-header">
		<div class="header-sticky">
			<nav class="navbar navbar-expand-lg">
				<div class="container-fluid">
					<!-- Logo Start -->
					<a class="navbar-brand" href="../">
						<img src="../images/gritsa-logo.svg" alt="Gritsa Technologies" style="height: 100px;">
					</a>
					<!-- Logo End -->

					<!-- Main Menu Start -->
					<div class="collapse navbar-collapse main-menu">
                        <div class="nav-menu-wrapper">
                            <ul class="navbar-nav mr-auto" id="menu">
                                <li class="nav-item"><a class="nav-link" href="../">Home</a></li>
                                <li class="nav-item"><a class="nav-link" href="../about/">About Us</a></li>
                                <li class="nav-item submenu"><a class="nav-link" href="../services/">Services</a>
                                    <ul>
                                        <li class="nav-item"><a class="nav-link" href="../services/">All Services</a></li>
                                        <li class="nav-item"><a class="nav-link" href="../services/development-as-a-service/">Development-as-a-Service</a></li>
                                        <li class="nav-item"><a class="nav-link" href="../services/developer-as-a-service/">Developer-as-a-Service</a></li>
                                        <li class="nav-item"><a class="nav-link" href="../services/ai-ml-solutions/">AI & ML Solutions</a></li>
                                    </ul>
                                </li>
                                <li class="nav-item"><a class="nav-link" href="../projects/">Projects</a></li>
                                <li class="nav-item"><a class="nav-link" href="../blog/">Blog</a></li>
                                <li class="nav-item"><a class="nav-link" href="../contact/">Contact</a></li>
                            </ul>
                        </div>
                        
                        <!-- Header Btn Start -->
                        <div class="header-btn">
                            <a href="../contact/" class="btn-default">Get Started</a>
                        </div>
                        <!-- Header Btn End -->
					</div>
					<!-- Main Menu End -->
					<div class="navbar-toggle"></div>
				</div>
			</nav>
			<div class="responsive-menu"></div>
		</div>
	</header>
	<!-- Header End -->'''
    
    # Standardized footer with ../ paths for subpages
    new_footer = '''    <footer class="main-footer">
        <!-- Footer Scrolling Ticker Section Start -->
        <div class="footer-scrolling-ticker">
            <!-- Scrolling Ticker Start -->
            <div class="footer-scrolling-box">
                <div class="scrolling-content">
                    <span><img src="../images/asterisk-icon.svg" alt="">Development-as-a-Service</span>
                    <span><img src="../images/asterisk-icon.svg" alt="">Developer-as-a-Service</span>
                    <span><img src="../images/asterisk-icon.svg" alt="">LLM & GPT Solutions</span>
                    <span><img src="../images/asterisk-icon.svg" alt="">AI Data Pipelines</span>
                    <span><img src="../images/asterisk-icon.svg" alt="">Development-as-a-Service</span>
                    <span><img src="../images/asterisk-icon.svg" alt="">Developer-as-a-Service</span>
                    <span><img src="../images/asterisk-icon.svg" alt="">LLM & GPT Solutions</span>
                    <span><img src="../images/asterisk-icon.svg" alt="">AI Data Pipelines</span>
                </div>

                <div class="scrolling-content">
                    <span><img src="../images/asterisk-icon.svg" alt="">Development-as-a-Service</span>
                    <span><img src="../images/asterisk-icon.svg" alt="">Developer-as-a-Service</span>
                    <span><img src="../images/asterisk-icon.svg" alt="">LLM & GPT Solutions</span>
                    <span><img src="../images/asterisk-icon.svg" alt="">AI Data Pipelines</span>
                    <span><img src="../images/asterisk-icon.svg" alt="">Development-as-a-Service</span>
                    <span><img src="../images/asterisk-icon.svg" alt="">Developer-as-a-Service</span>
                    <span><img src="../images/asterisk-icon.svg" alt="">LLM & GPT Solutions</span>
                    <span><img src="../images/asterisk-icon.svg" alt="">AI Data Pipelines</span>
                </div>
            </div>
            <!-- Scrolling Ticker End -->
        </div>
        <!-- Footer Scrolling Ticker Section End -->

        <!-- Footer Box Start -->
        <div class="footer-box bg-section">
            <div class="container">
                <div class="row">
                    <div class="col-lg-3">
                        <!-- About Footer Start -->
                        <div class="about-footer">
                            <!-- Footer Logo Start -->
                            <div class="footer-logo">
                                <img src="../images/gritsa-logo.svg" alt="Gritsa Technologies" style="height: 100px;">
                            </div>
                            <!-- Footer Logo End -->
                        </div>
                        <!-- About Footer End -->
                    </div>
        
                    <div class="col-lg-2 col-md-6">
                        <!-- Footer Links Start -->
                        <div class="footer-links">
                            <h3>quick link</h3>
                            <ul>
                                <li><a href="../">Home</a></li>
                                <li><a href="../about/">About Us</a></li>
                                <li><a href="../services/">Services</a></li>
                            </ul>
                        </div>
                        <!-- Footer Links End -->
                    </div>

                    <div class="col-lg-2 col-md-6">
                        <!-- Footer Links Start -->
                        <div class="footer-links">
                            <h3>Services</h3>
                            <ul>
                                <li><a href="../services/development-as-a-service/">Development-as-a-Service</a></li>
                                <li><a href="../services/developer-as-a-service/">Developer-as-a-Service</a></li>
                                <li><a href="../services/ai-ml-solutions/">AI & LLM Solutions</a></li>
                            </ul>
                        </div>
                        <!-- Footer Links End -->
                    </div>
        
                    <div class="col-lg-2 col-md-6">
                        <!-- Footer Links Start -->
                        <div class="footer-links">
                            <h3>Support</h3>
                            <ul>
                                <li><a href="../">Help</a></li>
                                <li><a href="../">Terms & Conditions </a></li>
                                <li><a href="../">Privacy Policy</a></li>
                            </ul>
                        </div>
                        <!-- Footer Links End -->
                    </div>
        
                    <div class="col-lg-3 col-md-6">
                        <!-- Footer Links Start -->
                        <div class="footer-links">
                            <h3>Get in Touch</h3>
                            <ul>
                                <li><a href="tel:+14242502424">+1 (424) 250-2424</a></li>
                                <li><a href="mailto:info@gritsa.com">info@gritsa.com</a></li>
                                <li>Unit A-132, Logix Technova<br>Sector-132, NOIDA (UP) 201301<br>India</li>
                            </ul>
                        </div>
                        <!-- Footer Links End -->
                    </div>
                </div>
            </div>
        </div>
        <!-- Footer Box End -->

        <!-- Footer Copyright Start -->
        <div class="footer-copyright">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-md-6">
                        <!-- Footer Copyright Text Start -->
                        <div class="footer-copyright-text">
                            <p>Copyright © 2011 - 2026 Gritsa Technologies. All Rights Reserved.</p>
                        </div>
                        <!-- Footer Copyright Text End -->
                    </div>
                    
                    <div class="col-md-6">
                        <!-- Footer Social Link Start -->
                        <div class="footer-social-links">
                            <ul>
                                <li><a href="https://www.facebook.com/GritsaTech/" target="_blank"><i class="fa-brands fa-facebook-f"></i></a></li>
                                <li><a href="https://in.linkedin.com/company/gritsa-technologies" target="_blank"><i class="fa-brands fa-linkedin-in"></i></a></li>
                                <li><a href="https://x.com/gritsa" target="_blank"><i class="fa-brands fa-x-twitter"></i></a></li>
                            </ul>
                        </div>
                        <!-- Footer Social Link End -->
                    </div>
                </div>
            </div>
        </div>
        <!-- Footer Copyright End -->
    </footer>
    <!-- Footer End -->'''
    
    # Replace header
    header_pattern = r'<div class="preloader">.*?<!-- Header End -->'
    content = re.sub(header_pattern, new_header, content, flags=re.DOTALL)
    
    # Replace footer
    footer_pattern = r'<footer class="main-footer">.*?</footer>\s*<!-- Footer End -->'
    content = re.sub(footer_pattern, new_footer, content, flags=re.DOTALL)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"✓ Updated {file_path}")

if __name__ == "__main__":
    pages = ['services', 'projects', 'blog', 'contact']
    for page in pages:
        update_page(page)
    print("All pages updated successfully!")
