import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: string | Date): string {
  return new Date(date).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

export function getMatchScoreColor(score: number): string {
  if (score >= 80) return 'text-green-600 bg-green-50'
  if (score >= 60) return 'text-blue-600 bg-blue-50'
  if (score >= 40) return 'text-yellow-600 bg-yellow-50'
  return 'text-red-600 bg-red-50'
}

export function truncate(str: string, length: number): string {
  return str.length > length ? str.substring(0, length) + '...' : str
}
