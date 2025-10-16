'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, X, FileText, Music } from 'lucide-react';

interface FileUploadProps {
  type: 'business-plan' | 'meeting-audio';
  files: File[];
  onFileUpload: (files: File[], type: 'business-plan' | 'meeting-audio') => void;
  onRemoveFile: (index: number, type: 'business-plan' | 'meeting-audio') => void;
}

const FileUpload = ({ type, files, onFileUpload, onRemoveFile }: FileUploadProps) => {
  const [activeTab, setActiveTab] = useState<'business-plan' | 'meeting-audio'>('business-plan');

  const onDrop = useCallback((acceptedFiles: File[]) => {
    onFileUpload(acceptedFiles, type);
  }, [onFileUpload, type]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: type === 'business-plan' 
      ? { 'application/pdf': ['.pdf'], 'application/msword': ['.doc'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'], 'application/vnd.ms-powerpoint': ['.ppt'], 'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'] }
      : { 'audio/mpeg': ['.mp3'], 'audio/wav': ['.wav'], 'audio/mp4': ['.m4a'], 'video/mp4': ['.mp4'] },
    multiple: true
  });

  const getFileIcon = (filename: string) => {
    const extension = filename.split('.').pop()?.toLowerCase();
    if (type === 'business-plan') {
      return <FileText className="w-6 h-6 text-blue-500" />;
    } else {
      return <Music className="w-6 h-6 text-green-500" />;
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getUploadText = () => {
    if (type === 'business-plan') {
      return {
        title: '사업계획서를 업로드하세요',
        description: 'PDF, Word, PowerPoint 파일 지원',
        hint: '클릭하거나 파일을 드래그해주세요'
      };
    } else {
      return {
        title: '미팅 오디오를 업로드하세요',
        description: 'MP3, WAV, M4A 파일 지원',
        hint: '클릭하거나 파일을 드래그해주세요'
      };
    }
  };

  const uploadText = getUploadText();

  return (
    <div className="mb-8">
      <div
        {...getRootProps()}
        className={`upload-area ${isDragActive ? 'dragover' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center">
          <Upload className="w-12 h-12 text-gray-400 mb-4" />
          <div className="text-lg font-semibold text-gray-700 mb-2">
            {uploadText.title}
          </div>
          <div className="text-sm text-gray-500 mb-1">
            {uploadText.description}
          </div>
          <div className="text-xs text-gray-400">
            {uploadText.hint}
          </div>
        </div>
      </div>

      {/* File List */}
      {files.length > 0 && (
        <div className="mt-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">업로드된 파일</h3>
          <div className="space-y-2">
            {files.map((file, index) => (
              <div key={index} className="flex items-center justify-between bg-white p-3 rounded-lg border border-gray-200">
                <div className="flex items-center space-x-3">
                  {getFileIcon(file.name)}
                  <div>
                    <div className="font-medium text-gray-900">{file.name}</div>
                    <div className="text-sm text-gray-500">{formatFileSize(file.size)}</div>
                  </div>
                </div>
                <button
                  onClick={() => onRemoveFile(index, type)}
                  className="text-red-500 hover:text-red-700 p-1"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
