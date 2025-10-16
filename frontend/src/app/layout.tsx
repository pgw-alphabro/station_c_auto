import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Station C 2025 AI 진단보고서',
  description: 'AI 기반 자동 진단보고서 생성 시스템',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  )
}