import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'app_gym';
  isAlertVisible = true;
  isAlertClosing = false;

  ngOnInit(): void {
    setTimeout(() => {
      this.hideAlert();
    }, 5000);
  }

  hideAlert(): void {
    this.isAlertClosing = true;
    setTimeout(() => {
      this.isAlertVisible = false;
    }, 500);
  }
}
