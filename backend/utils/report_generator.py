from weasyprint import HTML
import jinja2
import os
from datetime import datetime
from models.schemas import ScreeningResponse

class ReportGenerator:
    def __init__(self, template_dir="backend/utils/templates"):
        self.template_dir = template_dir
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)
            
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.template_dir))
        
        # Create a default template if it doesn't exist
        self.template_path = os.path.join(self.template_dir, "compliance_report.html")
        if not os.path.exists(self.template_path):
            with open(self.template_path, "w") as f:
                f.write("""
                <html>
                <head>
                    <style>
                        body { font-family: sans-serif; }
                        h1 { color: #2c3e50; }
                        .status { font-weight: bold; }
                        .PASSED { color: green; }
                        .VIOLATION_DETECTED { color: red; }
                        table { width: 100%; border-collapse: collapse; }
                        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                        th { background-color: #f2f2f2; }
                    </style>
                </head>
                <body>
                    <h1>Compliance Screening Audit Report</h1>
                    <p><strong>Order ID:</strong> {{ order_id }}</p>
                    <p><strong>Status:</strong> <span class="status {{ overall_status }}">{{ overall_status }}</span></p>
                    <p><strong>Generated At:</strong> {{ timestamp }}</p>
                    
                    <h2>Detailed Checks</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Check Name</th>
                                <th>Status</th>
                                <th>Details</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for check in checks %}
                            <tr>
                                <td>{{ check.check_name }}</td>
                                <td class="{{ check.status }}">{{ check.status }}</td>
                                <td>{{ check.details }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </body>
                </html>
                """)

    async def generate_pdf(self, screening_data: ScreeningResponse) -> str:
        template = self.env.get_template("compliance_report.html")
        html_content = template.render(
            order_id=screening_data.order_id,
            overall_status=screening_data.overall_status,
            checks=screening_data.checks,
            timestamp=screening_data.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        output_dir = "backend/tests/reports"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        file_path = f"{output_dir}/{screening_data.report_id}.pdf"
        HTML(string=html_content).write_pdf(file_path)
        return file_path

report_generator = ReportGenerator()
