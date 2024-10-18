from django.shortcuts import render
from .models import PenetrationTest
from django.http import JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from django.conf import settings
from datetime import datetime
import os
import base64


# Create your views here.
def index(request):
    print("Go to index view of planning phase")
    if request.method == "POST":
        data = request.POST
        try:
            # Handle Primary Contact Signature
            target_signature_data = data.get("target-signature")
            if target_signature_data:
                target_signature_data = target_signature_data.replace(
                    "data:image/png;base64,", ""
                )
                target_signature_image = base64.b64decode(target_signature_data)
                target_signature_path = os.path.join(
                    settings.SIGNATURES_DIRECTORY, "target_signature.png"
                )
                with open(target_signature_path, "wb") as img_file:
                    img_file.write(target_signature_image)

            # Handle Pen Test Leader Signature
            pen_test_leader_signature_data = data.get("pen-test-leader")
            if pen_test_leader_signature_data:
                pen_test_leader_signature_data = pen_test_leader_signature_data.replace(
                    "data:image/png;base64,", ""
                )
                pen_test_leader_signature_image = base64.b64decode(
                    pen_test_leader_signature_data
                )
                pen_test_leader_signature_path = os.path.join(
                    settings.SIGNATURES_DIRECTORY, "pen_test_leader_signature.png"
                )
                with open(pen_test_leader_signature_path, "wb") as img_file:
                    img_file.write(pen_test_leader_signature_image)

            # Create the PenetrationTest instance
            penetration_test = PenetrationTest(
                team_primary_contact=data.get("team-primary-contact"),
                team_primary_phone=data.get("team-primary-phone"),
                team_primary_pager=data.get("team-primary-pager"),
                team_secondary_contact=data.get("team-secondary-contact"),
                team_secondary_phone=data.get("team-secondary-phone"),
                team_secondary_pager=data.get("team-secondary-pager"),
                target_primary_contact=data.get("target-primary-contact"),
                target_primary_phone=data.get("target-primary-phone"),
                target_primary_pager=data.get("target-primary-pager"),
                target_secondary_contact=data.get("target-secondary-contact"),
                target_secondary_phone=data.get("target-secondary-phone"),
                target_secondary_pager=data.get("target-secondary-pager"),
                debrief_frequency=data.get("debrief-frequency"),
                debrief_location=data.get("debrief-location"),
                start_date=data.get("start-date"),
                end_date=data.get("end-date"),
                test_times=data.get("test-times"),
                announced_test=data.get("announced-test"),
                shun_ip=data.get("shun-ip"),
                automatic_shun=data.get("automatic-shun"),
                shun_steps=data.get("shun-steps"),
                conclude_test=data.get("conclude-test"),
                continue_test=data.get("continue-test"),
                attack_ips=data.get("attack-ips"),
                black_box=data.get("black-box"),
                viewing_policy=data.get("viewing-policy"),
                observing_team=data.get("observing-team"),
                target_signature=data.get("target-signature"),
                target_date=data.get("target-date"),
                pen_test_leader=data.get("pen-test-leader"),
                leader_date=data.get("leader-date"),
                tester_signatures=data.get("tester-signatures"),
                target_signature_image=target_signature_path,
                pen_test_leader_signature_image=pen_test_leader_signature_path,
            )
            # Attempt to save the instance
            penetration_test.save()

            # Generate PDF
            pdf_file_path = generate_pdf(penetration_test)

            # Prepare the response
            pdf_file_name = os.path.basename(pdf_file_path)
            print(f"pdf_file_name is: {pdf_file_name}")

            return JsonResponse(
                {
                    "status": "success",
                    "message": "planning and scoping details saved successfully.",
                    "pdf_file_name": pdf_file_name,  # Return the PDF file name
                },
                status=201,  # HTTP 201 Created
            )

        except ValueError as ve:
            print("Go here mean error type 1")
            # Handle specific value errors (e.g., validation errors)
            return JsonResponse(
                {"status": "error", "message": f"Value error: {str(ve)}"}, status=400
            )  # HTTP 400 Bad Request

        except Exception as e:
            print("Go here mean error type 2")
            # Handle unexpected errors
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"An unexpected error occurred: {str(e)}",
                },
                status=500,
            )  # HTTP 500 Internal Server Error

    return render(request, "planning/index.html")


def generate_pdf(penetration_test):
    """Generate a PDF report based on the penetration test data."""
    print("Go to function generate_pdf")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_file_name = f"planning_scoping_{penetration_test.id}_{timestamp}.pdf"
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, pdf_file_name)

    try:
        # Create the PDF file
        c = canvas.Canvas(pdf_file_path, pagesize=letter)

        # Title
        title = "Penetration Testing Rules Of Engagement"
        width, height = letter
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2, 750, title)

        # Function to draw section titles
        def draw_section_title(y, title_text):
            c.setFillColor(colors.blue)  # Set the color for the section title
            c.setFont("Helvetica-Bold", 14)
            c.drawString(100, y, title_text)
            c.setFillColor(colors.black)  # Reset to black for content
            c.setFont("Helvetica", 12)

        # Define maximum height for content to fit on the page
        MAX_HEIGHT = height - 100  # Reserve space for title and margin
        current_y = 720  # Starting y position

        # List of sections to include in the PDF
        sections = [
            (
                "Team Primary Contact",
                [
                    f"Primary Contact: {penetration_test.team_primary_contact}",
                    f"Mobile Phone: {penetration_test.team_primary_phone}",
                    f"Pager: {penetration_test.team_primary_pager}",
                ],
            ),
            (
                "Team Secondary Contact",
                [
                    f"Secondary Contact: {penetration_test.team_secondary_contact}",
                    f"Secondary Phone: {penetration_test.team_secondary_phone}",
                    f"Secondary Pager: {penetration_test.team_secondary_pager}",
                ],
            ),
            (
                "Target Primary Contact",
                [
                    f"Target Primary Contact: {penetration_test.target_primary_contact}",
                    f"Target Phone: {penetration_test.target_primary_phone}",
                    f"Target Pager: {penetration_test.target_primary_pager}",
                ],
            ),
            (
                "Target Secondary Contact",
                [
                    f"Target Secondary Contact: {penetration_test.target_secondary_contact}",
                    f"Target Secondary Phone: {penetration_test.target_secondary_phone}",
                    f"Target Secondary Pager: {penetration_test.target_secondary_pager}",
                ],
            ),
            (
                "Debriefing Information",
                [
                    f"Debrief Frequency: {penetration_test.debrief_frequency}",
                    f"Debrief Location: {penetration_test.debrief_location}",
                ],
            ),
            (
                "Test Dates and Times",
                [
                    f"Start Date: {penetration_test.start_date}",
                    f"End Date: {penetration_test.end_date}",
                    f"Test Times: {penetration_test.test_times}",
                ],
            ),
            (
                "Testing Parameters",
                [
                    f"Announced Test: {penetration_test.announced_test}",
                    f"Shun IP: {penetration_test.shun_ip}",
                    f"Automatic Shun: {penetration_test.automatic_shun}",
                    f"Shun Steps: {penetration_test.shun_steps}",
                ],
            ),
            (
                "Test Continuation Information",
                [
                    f"Conclude Test: {penetration_test.conclude_test}",
                    f"Continue Test: {penetration_test.continue_test}",
                ],
            ),
            (
                "Attack and Policy Information",
                [
                    f"Attack IPs: {penetration_test.attack_ips}",
                    f"Black Box: {penetration_test.black_box}",
                    f"Viewing Policy: {penetration_test.viewing_policy}",
                    f"Observing Team: {penetration_test.observing_team}",
                ],
            ),
            (
                "Signature Information",
                [
                    #     f"Target Signature: {penetration_test.target_signature}",
                    #     f"Target Date: {penetration_test.target_date}",
                    #     f"Pen Test Leader: {penetration_test.pen_test_leader}",
                    #     f"Leader Date: {penetration_test.leader_date}",
                    #     f"Tester Signatures: {penetration_test.tester_signatures}",
                ],
            ),
        ]

        # Loop through sections and draw them
        for section_title, content in sections:
            if current_y < 100:  # If there's not enough space for a new section
                c.showPage()  # Create a new page
                current_y = 720  # Reset position

            draw_section_title(current_y, section_title)
            current_y -= 20  # Move down after the title

            for line in content:
                c.drawString(100, current_y, line)
                current_y -= 20  # Move down for the next line

        # Target Signature
        if penetration_test.target_signature:
            c.drawString(100, current_y, "Target Signature:")
            current_y -= 100  # Move down for image

            # Debugging: Print image path
            target_image_path = penetration_test.target_signature_image.path
            print(f"Target signature image path: {target_image_path}")

            c.drawImage(
                target_image_path,  # Use .path to get the full file path
                100,
                current_y,
                width=200,
                height=100,
                mask="auto",  # Automatically manage transparency
            )
            current_y -= 40  # Move down for the next section

        # Target Date
        if penetration_test.target_date:
            c.drawString(100, current_y, f"Target Date: {penetration_test.target_date}")
            current_y -= 50  # Move down for the next entry

        # Pen Test Leader Signature
        if penetration_test.pen_test_leader:
            c.drawString(100, current_y, "Pen Test Leader Signature:")
            current_y -= 100  # Move down for image

            # Debugging: Print image path
            leader_image_path = penetration_test.pen_test_leader_signature_image.path
            print(f"Pen test leader signature image path: {leader_image_path}")

            c.drawImage(
                leader_image_path,  # Use .path to get the full file path
                100,
                current_y,
                width=200,
                height=100,
                mask="auto",  # Automatically manage transparency
            )
            current_y -= 40  # Move down for the next section

        # Leader Date
        if penetration_test.leader_date:
            c.drawString(100, current_y, f"Leader Date: {penetration_test.leader_date}")
            current_y -= 50  # Move down for the next entry

        # Tester Signatures
        if penetration_test.tester_signatures:
            c.drawString(100, current_y, "Tester Signatures:")
            current_y -= 30  # Move down for the signatures
            tester_signatures_list = (
                penetration_test.tester_signatures.splitlines()
            )  # Assuming they are newline-separated

            for signature in tester_signatures_list:
                c.drawString(100, current_y, signature)
                current_y -= 20  # Move down for the next tester signature

        # Save the PDF
        c.save()
    except Exception as e:
        print(f"An error occurred while generating the PDF: {e}")
        # You may want to raise the exception or handle it differently depending on your needs
        raise  # Reraise the exception for further handling if needed

    return pdf_file_path
