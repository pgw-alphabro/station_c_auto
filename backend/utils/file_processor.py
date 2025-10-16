import os
import pytesseract
from PIL import Image
import PyPDF2
from docx import Document

def extract_text_from_file(file_path: str) -> str:
    """파일에서 텍스트 추출 (PDF, DOCX, 이미지 지원)"""
    try:
        file_extension = file_path.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            return extract_text_from_pdf(file_path)
        elif file_extension in ['docx', 'doc']:
            return extract_text_from_docx(file_path)
        elif file_extension == 'hwp':
            return extract_text_from_hwp(file_path)
        elif file_extension in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
            return extract_text_from_image(file_path)
        elif file_extension == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f"지원하지 않는 파일 형식: {file_extension}"
    except Exception as e:
        return f"파일 처리 중 오류 발생: {str(e)}"

def extract_text_from_pdf(file_path: str) -> str:
    """PDF에서 텍스트 추출"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"PDF 처리 오류: {str(e)}"

def extract_text_from_docx(file_path: str) -> str:
    """DOCX에서 텍스트 추출"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"DOCX 처리 오류: {str(e)}"

def extract_text_from_hwp(file_path: str) -> str:
    """HWP 파일에서 텍스트 추출 (hwp5txt의 TextTransform 직접 사용)"""
    try:
        from hwp5.hwp5txt import TextTransform
        from hwp5.xmlmodel import Hwp5File
        from contextlib import closing
        import io
        
        # TextTransform을 사용해서 텍스트 추출
        try:
            text_transform = TextTransform()
            transform = text_transform.transform_hwp5_to_text
            
            # BytesIO를 사용해서 출력 캡처
            output = io.BytesIO()
            
            # HWP 파일을 열고 텍스트로 변환
            with closing(Hwp5File(file_path)) as hwp5file:
                transform(hwp5file, output)
            
            # 추출된 텍스트 가져오기 (bytes를 문자열로 변환)
            extracted_text = output.getvalue().decode('utf-8', errors='ignore')
            output.close()
            
            if extracted_text.strip():
                return extracted_text.strip()
            else:
                return "HWP 파일에서 텍스트를 추출할 수 없습니다."
                
        except Exception as e:
            print(f"hwp5txt TextTransform 오류: {e}")
            return extract_text_from_hwp_fallback(file_path)
                
    except Exception as e:
        print(f"hwp5txt 라이브러리 오류: {e}")
        return extract_text_from_hwp_fallback(file_path)

def extract_text_from_hwp_fallback(file_path: str) -> str:
    """HWP 파일 텍스트 추출 (대체 방법)"""
    try:
        # HWP 파일을 바이너리로 읽어서 패턴 매칭으로 텍스트 추출
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # UTF-8로 디코딩
        decoded = content.decode('utf-8', errors='ignore')
        
        # 한글 텍스트 패턴 찾기 (연속된 한글 3글자 이상)
        import re
        korean_patterns = re.findall(r'[가-힣]{3,}', decoded)
        
        if korean_patterns:
            # 의미있는 문장들만 추출
            sentences = []
            for pattern in korean_patterns:
                if len(pattern) > 5:  # 최소 5글자 이상
                    sentences.append(pattern)
            
            if sentences:
                return ' '.join(sentences[:50])  # 최대 50개 문장
            else:
                return "HWP 파일에서 의미있는 텍스트를 찾을 수 없습니다."
        else:
            return "HWP 파일에서 한글 텍스트를 찾을 수 없습니다."
            
    except Exception as e:
        return f"HWP 대체 처리 오류: {str(e)}"

def extract_text_from_image(file_path: str) -> str:
    """이미지에서 OCR로 텍스트 추출"""
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang='kor+eng')
        return text
    except Exception as e:
        return f"OCR 처리 오류: {str(e)}"
