from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, Frame, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Circle, Rect, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from django.conf import settings
import os
import json
from datetime import datetime
from PIL import Image as PILImage
import io

def generate_interview_pdf(interview):
    """Generate a beautiful dashboard-style PDF report for interview results"""
    
    # Create PDF buffer
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Dashboard styles
    title_style = ParagraphStyle(
        'DashboardTitle',
        parent=styles['Heading1'],
        fontSize=28,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.white,
        backColor=colors.HexColor('#1e3a8a')
    )
    
    header_style = ParagraphStyle(
        'DashboardHeader',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=12,
        textColor=colors.HexColor('#1e40af'),
        fontName='Helvetica-Bold'
    )
    
    metric_style = ParagraphStyle(
        'MetricStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#374151')
    )
    
    content_style = ParagraphStyle(
        'DashboardContent',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=8,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#4b5563')
    )
    
    # Story elements
    story = []
    
    # Dashboard Header with background
    header_table = Table([['AI Interview Dashboard']], colWidths=[7*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 24),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ('ROUNDEDCORNERS', [10, 10, 10, 10]),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 25))
    
    # Dashboard Info Cards
    info_data = [
        ['Candidate', 'Position', 'Company'],
        [interview.candidate_name, interview.job.title, interview.job.company],
        ['Date', 'ID', 'Status'],
        [interview.completed_at.strftime('%b %d, %Y') if interview.completed_at else 'N/A', 
         str(interview.uuid)[:8], interview.get_status_display()]
    ]
    
    info_table = Table(info_data, colWidths=[2.3*inch, 2.3*inch, 2.3*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#6366f1')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0, 3), (-1, 3), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTNAME', (0, 3), (-1, 3), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 2), (-1, 2), 9),
        ('FONTSIZE', (0, 1), (-1, 1), 12),
        ('FONTSIZE', (0, 3), (-1, 3), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 25))
    
    # Performance Dashboard with Visual Elements
    story.append(Paragraph("Performance dashboard", header_style))
    story.append(Spacer(1, 15))
    
    # Score Cards Layout
    scores = [
        ('Overall', interview.overall_score or 0, colors.HexColor('#3b82f6')),
        ('Technical', interview.technical_score or 0, colors.HexColor('#10b981')),
        ('Communication', interview.communication_score or 0, colors.HexColor('#f59e0b')),
        ('Problem solving', interview.problem_solving_score or 0, colors.HexColor('#8b5cf6'))
    ]
    
    # Create score cards in 2x2 grid
    score_cards = []
    for i in range(0, len(scores), 2):
        row_data = []
        for j in range(2):
            if i + j < len(scores):
                label, score, color = scores[i + j]
                score_text = f"{score:.1f}/10"
                rating = get_rating(score)
                card_content = f"{label}\n{score_text}\n{rating}"
                row_data.append(card_content)
            else:
                row_data.append('')
        score_cards.append(row_data)
    
    score_table = Table(score_cards, colWidths=[3.5*inch, 3.5*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#dbeafe')),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#d1fae5')),
        ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#fef3c7')),
        ('BACKGROUND', (1, 1), (1, 1), colors.HexColor('#e9d5ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('GRID', (0, 0), (-1, -1), 2, colors.HexColor('#e2e8f0')),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
    ]))
    
    story.append(score_table)
    story.append(Spacer(1, 25))
    
    # Hiring Decision Banner
    rec_color = get_recommendation_color(interview.recommendation)
    rec_text = interview.get_recommendation_display() if interview.recommendation else 'No Recommendation'
    rec_icon = get_recommendation_icon(interview.recommendation)
    
    decision_data = [[f'Hiring decision: {rec_text}']]
    decision_table = Table(decision_data, colWidths=[7*inch])
    decision_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), rec_color),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 18),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 18),
        ('ROUNDEDCORNERS', [10, 10, 10, 10]),
    ]))
    
    story.append(decision_table)
    story.append(Spacer(1, 20))
    
    # Candidate Feedback Quote Box
    if interview.ai_feedback:
        # Extract feedback section from AI analysis
        feedback_lines = interview.ai_feedback.split('\n')
        candidate_feedback = ""
        
        # Find "Feedback for the Candidate:" section
        feedback_started = False
        for line in feedback_lines:
            if 'feedback for the candidate' in line.lower():
                feedback_started = True
                continue
            if feedback_started:
                if line.strip() and not line.startswith('Overall') and not line.startswith('Decision'):
                    candidate_feedback += line.strip() + " "
        
        if not candidate_feedback:
            # Fallback: use last paragraph of AI feedback
            feedback_paragraphs = [p.strip() for p in interview.ai_feedback.split('\n\n') if p.strip()]
            if feedback_paragraphs:
                candidate_feedback = feedback_paragraphs[-1]
        
        if candidate_feedback:
            # Make feedback more compact
            if len(candidate_feedback) > 300:
                sentences = candidate_feedback.split('. ')
                candidate_feedback = '. '.join(sentences[:2]) + '.'
            
            # Create wrapped paragraph for feedback
            feedback_paragraph = Paragraph(f'"{candidate_feedback.strip()}"', ParagraphStyle(
                'FeedbackText',
                parent=content_style,
                fontSize=11,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#92400e'),
                fontName='Helvetica-Oblique',
                leading=14
            ))
            
            feedback_data = [
                ['Feedback for the candidate from AI interviewer'],
                [feedback_paragraph]
            ]
            feedback_table = Table(feedback_data, colWidths=[6.5*inch])
            feedback_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f59e0b')),
                ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#fef7cd')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#92400e')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Oblique'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTSIZE', (0, 1), (-1, 1), 11),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 1), (-1, 1), 15),
                ('BOTTOMPADDING', (0, 1), (-1, 1), 15),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                ('GRID', (0, 0), (-1, -1), 2, colors.HexColor('#f59e0b')),
                ('ROUNDEDCORNERS', [8, 8, 8, 8]),
            ]))
            
            story.append(feedback_table)
            story.append(Spacer(1, 25))
    
    # Interview Statistics Cards
    try:
        questions = json.loads(interview.questions_asked) if interview.questions_asked else []
        answers = json.loads(interview.answers_given) if interview.answers_given else []
        total_q = len(questions)
        total_a = len(answers)
        response_rate = f"{(total_a/total_q*100):.0f}%" if total_q > 0 else "0%"
    except:
        total_q, total_a, response_rate = 0, 0, "0%"
    
    stats_data = [
        ['Questions asked', 'Responses given', 'Response rate'],
        [str(total_q), str(total_a), response_rate]
    ]
    
    stats_table = Table(stats_data, colWidths=[2.3*inch, 2.3*inch, 2.3*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f9fafb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#1f2937')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, 1), 18),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
    ]))
    
    story.append(stats_table)
    story.append(Spacer(1, 20))
    
    # Add first screenshot to first page
    if interview.screenshots_data:
        try:
            screenshots = json.loads(interview.screenshots_data)
            if screenshots:
                first_screenshot = screenshots[0]
                screenshot_path = os.path.join(settings.MEDIA_ROOT, first_screenshot['path'])
                if os.path.exists(screenshot_path):
                    try:
                        img = PILImage.open(screenshot_path)
                        img.thumbnail((300, 200), PILImage.Resampling.LANCZOS)
                        
                        img_buffer = io.BytesIO()
                        img.save(img_buffer, format='JPEG')
                        img_buffer.seek(0)
                        
                        # Create image box
                        img_data = [[
                            'Interview visual sample',
                            Image(img_buffer, width=2.5*inch, height=1.7*inch)
                        ]]
                        
                        img_table = Table(img_data, colWidths=[1.5*inch, 2.5*inch])
                        img_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
                            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (0, 0), 10),
                            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
                            ('TOPPADDING', (0, 0), (-1, -1), 10),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                        ]))
                        
                        story.append(img_table)
                        story.append(Spacer(1, 15))
                        
                    except Exception as e:
                        pass
        except (json.JSONDecodeError, TypeError):
            pass
    
    story.append(Spacer(1, 10))
    
    # AI Analysis Section (without candidate feedback)
    if interview.ai_feedback:
        story.append(Paragraph("AI analysis and insights", header_style))
        
        # Extract only analysis parts (exclude candidate feedback)
        analysis_text = interview.ai_feedback
        if 'feedback for the candidate' in analysis_text.lower():
            analysis_parts = analysis_text.split('Feedback for the Candidate:')
            analysis_text = analysis_parts[0].strip()
        
        # Create wrapped paragraph for analysis
        analysis_paragraph = Paragraph(analysis_text, ParagraphStyle(
            'AnalysisText',
            parent=content_style,
            fontSize=10,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#0c4a6e'),
            leading=12
        ))
        
        # Create analysis box
        analysis_data = [[analysis_paragraph]]
        analysis_table = Table(analysis_data, colWidths=[6.5*inch])
        analysis_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f9ff')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#0c4a6e')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('GRID', (0, 0), (-1, -1), 2, colors.HexColor('#0ea5e9')),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ]))
        
        story.append(analysis_table)
        story.append(Spacer(1, 20))
    
    # Q&A Section with Bubble Style
    if interview.questions_asked and interview.answers_given:
        story.append(PageBreak())
        story.append(Paragraph("Interview conversation", header_style))
        story.append(Spacer(1, 15))
        
        try:
            questions = json.loads(interview.questions_asked)
            answers = json.loads(interview.answers_given)
            
            for i, (q, a) in enumerate(zip(questions, answers), 1):
                # Interviewer bubble (left aligned)
                q_text = q.get('question', 'Question not recorded')
                q_paragraph = Paragraph(f"Interviewer: {q_text}", ParagraphStyle(
                    'InterviewerBubble',
                    parent=content_style,
                    fontSize=10,
                    alignment=TA_LEFT,
                    textColor=colors.HexColor('#1e40af'),
                    leading=12,
                    leftIndent=10,
                    rightIndent=50
                ))
                
                q_table = Table([[q_paragraph]], colWidths=[6*inch])
                q_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#dbeafe')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                    ('LEFTPADDING', (0, 0), (-1, -1), 15),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                    ('ROUNDEDCORNERS', [10, 10, 10, 10]),
                ]))
                
                story.append(q_table)
                story.append(Spacer(1, 8))
                
                # Candidate bubble (right aligned)
                a_text = a.get('answer', 'Answer not recorded')
                a_paragraph = Paragraph(f"Candidate: {a_text}", ParagraphStyle(
                    'CandidateBubble',
                    parent=content_style,
                    fontSize=10,
                    alignment=TA_LEFT,
                    textColor=colors.HexColor('#065f46'),
                    leading=12,
                    leftIndent=50,
                    rightIndent=10
                ))
                
                a_table = Table([['', a_paragraph]], colWidths=[1*inch, 5*inch])
                a_table.setStyle(TableStyle([
                    ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#d1fae5')),
                    ('ALIGN', (1, 0), (1, 0), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (1, 0), (1, 0), 10),
                    ('BOTTOMPADDING', (1, 0), (1, 0), 10),
                    ('LEFTPADDING', (1, 0), (1, 0), 15),
                    ('RIGHTPADDING', (1, 0), (1, 0), 15),
                    ('ROUNDEDCORNERS', [10, 10, 10, 10]),
                ]))
                
                story.append(a_table)
                story.append(Spacer(1, 12))
                
        except (json.JSONDecodeError, TypeError):
            error_paragraph = Paragraph("Conversation data could not be parsed.", content_style)
            story.append(error_paragraph)
    
    # Screenshots Gallery
    if interview.screenshots_data:
        try:
            screenshots = json.loads(interview.screenshots_data)
            if screenshots:
                story.append(PageBreak())
                story.append(Paragraph("Interview visual evidence", header_style))
                story.append(Spacer(1, 15))
                
                # Sort screenshots by timestamp
                sorted_screenshots = sorted(screenshots, key=lambda x: x.get('timestamp', ''))
                
                # Create timeline of screenshots
                for i, screenshot in enumerate(sorted_screenshots[:6]):  # Limit to 6 screenshots
                    screenshot_path = os.path.join(settings.MEDIA_ROOT, screenshot['path'])
                    if os.path.exists(screenshot_path):
                        try:
                            img = PILImage.open(screenshot_path)
                            img.thumbnail((300, 200), PILImage.Resampling.LANCZOS)
                            
                            img_buffer = io.BytesIO()
                            img.save(img_buffer, format='JPEG')
                            img_buffer.seek(0)
                            
                            # Create timestamp and image row
                            timestamp = screenshot.get('timestamp', 'Unknown')[:19]
                            reason = screenshot.get('reason', 'scheduled')
                            
                            img_data = [[
                                f"Time: {timestamp}\nReason: {reason}",
                                Image(img_buffer, width=2.5*inch, height=1.7*inch)
                            ]]
                            
                            img_table = Table(img_data, colWidths=[2*inch, 2.5*inch])
                            img_table.setStyle(TableStyle([
                                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
                                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                ('FONTNAME', (0, 0), (0, 0), 'Helvetica'),
                                ('FONTSIZE', (0, 0), (0, 0), 9),
                                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
                                ('TOPPADDING', (0, 0), (-1, -1), 8),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                            ]))
                            
                            story.append(img_table)
                            story.append(Spacer(1, 10))
                            
                        except Exception as e:
                            pass
                            
        except (json.JSONDecodeError, TypeError):
            pass
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

def get_rating(score):
    """Convert numeric score to rating"""
    if score >= 8:
        return "Excellent"
    elif score >= 6:
        return "Good"
    elif score >= 4:
        return "Average"
    else:
        return "Poor"

def get_recommendation_color(recommendation):
    """Get color for recommendation"""
    colors_map = {
        'highly_recommended': colors.HexColor('#059669'),
        'recommended': colors.HexColor('#0ea5e9'),
        'maybe': colors.HexColor('#d97706'),
        'not_recommended': colors.HexColor('#dc2626'),
        'never_hire': colors.HexColor('#7f1d1d')
    }
    return colors_map.get(recommendation, colors.HexColor('#6b7280'))

def get_recommendation_icon(recommendation):
    """Get icon for recommendation"""
    return ''  # No icons needed