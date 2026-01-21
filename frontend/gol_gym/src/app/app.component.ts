import { Component, OnInit, OnDestroy } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'app_gym';
  isAlertVisible = true;
  isAlertClosing = false;
  isAlertPaused = false;

  private timeoutId: ReturnType<typeof setTimeout> | null = null;
  private remainingTime = 5000;
  private startTime = 0;

  ngOnInit(): void {
    this.startTimer();
  }

  ngOnDestroy(): void {
    this.clearTimer();
  }

  private startTimer(): void {
    this.startTime = Date.now();
    this.timeoutId = setTimeout(() => {
      this.hideAlert();
    }, this.remainingTime);
  }

  private clearTimer(): void {
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
      this.timeoutId = null;
    }
  }

  pauseTimer(): void {
    if (!this.isAlertPaused && !this.isAlertClosing) {
      this.clearTimer();
      this.remainingTime -= Date.now() - this.startTime;
      this.isAlertPaused = true;
    }
  }

  resumeTimer(): void {
    if (this.isAlertPaused && !this.isAlertClosing) {
      this.isAlertPaused = false;
      this.startTimer();
    }
  }

  hideAlert(): void {
    this.clearTimer();
    this.isAlertClosing = true;
    setTimeout(() => {
      this.isAlertVisible = false;
    }, 500);
  }
}
