import { useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { AlertCircle, CheckCircle2, Info, XCircle, X } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';

export type StatusType = 'info' | 'success' | 'warning' | 'error';

interface StatusBannerProps {
  type: StatusType;
  title: string;
  message: string;
  duration?: number;
  isVisible: boolean;
  onClose: () => void;
}

const statusConfig = {
  info: {
    icon: <Info className="h-4 w-4" />,
    variant: 'default' as const,
    className: 'border-blue-500/50 bg-blue-500/10 text-blue-700 dark:text-blue-400',
  },
  success: {
    icon: <CheckCircle2 className="h-4 w-4" />,
    variant: 'default' as const,
    className: 'border-green-500/50 bg-green-500/10 text-green-700 dark:text-green-400',
  },
  warning: {
    icon: <AlertCircle className="h-4 w-4" />,
    variant: 'default' as const,
    className: 'border-amber-500/50 bg-amber-500/10 text-amber-700 dark:text-amber-400',
  },
  error: {
    icon: <XCircle className="h-4 w-4" />,
    variant: 'destructive' as const,
    className: '',
  },
};

export function StatusBanner({ 
  type, 
  title, 
  message, 
  duration = 5000, 
  isVisible,
  onClose 
}: StatusBannerProps) {
  useEffect(() => {
    if (isVisible && duration > 0) {
      const timer = setTimeout(onClose, duration);
      return () => clearTimeout(timer);
    }
  }, [isVisible, duration, onClose]);

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="fixed top-4 left-1/2 z-[100] w-full max-w-md -translate-x-1/2 px-4"
        >
          <Alert variant={statusConfig[type].variant} className={statusConfig[type].className}>
            {statusConfig[type].icon}
            <AlertTitle>{title}</AlertTitle>
            <AlertDescription className="flex items-center justify-between gap-4">
              <span>{message}</span>
              <Button
                variant="ghost"
                size="icon-sm"
                className="h-6 w-6 shrink-0 opacity-70 hover:opacity-100"
                onClick={onClose}
              >
                <X className="h-4 w-4" />
              </Button>
            </AlertDescription>
          </Alert>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
