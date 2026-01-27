#!/usr/bin/env python3
import re

# The standardized footer ticker
ticker = '''            <!-- Scrolling Ticker Start -->
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
            <!-- Scrolling Ticker End -->'''

# Update each file
for page in ['projects', 'blog', 'contact']:
    filepath = f"{page}/index.html"
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace the ticker section
    content = re.sub(
        r'<!-- Scrolling Ticker Start -->.*?<!-- Scrolling Ticker End -->',
        ticker.strip(),
        content,
        flags=re.DOTALL
    )
    
    # Fix service links in footer
    content = re.sub(
        r'<li><a href="service-single.html">AI Development</a></li>',
        '<li><a href="../services/development-as-a-service/">Development-as-a-Service</a></li>',
        content
    )
    content = re.sub(
        r'<li><a href="service-single.html">Machine Learning</a></li>',
        '<li><a href="../services/developer-as-a-service/">Developer-as-a-Service</a></li>',
        content
    )
    content = re.sub(
        r'<li><a href="service-single.html">Predictive Analytics</a></li>',
        '<li><a href="../services/ai-ml-solutions/">AI & LLM Solutions</a></li>',
        content
    )
    
    # Fix support links
    content = re.sub(
        r'<li><a href="[a-z]+\.html#">Help</a></li>',
        '<li><a href="../">Help</a></li>',
        content
    )
    content = re.sub(
        r'<li><a href="[a-z]+\.html#">Terms & Conditions </a></li>',
        '<li><a href="../">Terms & Conditions </a></li>',
        content
    )
    content = re.sub(
        r'<li><a href="[a-z]+\.html#">Privacy Policy</a></li>',
        '<li><a href="../">Privacy Policy</a></li>',
        content
    )
    
    # Fix social links
    content = re.sub(
        r'<li><a href="[a-z]+\.html#"><i class="fa-brands fa-pinterest-p"></i></a></li>',
        '<li><a href="https://www.facebook.com/GritsaTech/" target="_blank"><i class="fa-brands fa-facebook-f"></i></a></li>',
        content
    )
    content = re.sub(
        r'<li><a href="[a-z]+\.html#"><i class="fa-brands fa-x-twitter"></i></a></li>',
        '<li><a href="https://x.com/gritsa" target="_blank"><i class="fa-brands fa-x-twitter"></i></a></li>',
        content
    )
    content = re.sub(
        r'<li><a href="[a-z]+\.html#"><i class="fa-brands fa-facebook-f"></i></a></li>',
        '<li><a href="https://in.linkedin.com/company/gritsa-technologies" target="_blank"><i class="fa-brands fa-linkedin-in"></i></a></li>',
        content
    )
    content = re.sub(
        r'<li><a href="[a-z]+\.html#"><i class="fa-brands fa-instagram"></i></a></li>',
        '',
        content
    )
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"✓ Updated {filepath}")

print("All footers updated!")
