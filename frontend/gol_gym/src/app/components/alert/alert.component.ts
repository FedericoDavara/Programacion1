import { Component } from '@angular/core';

@Component({
  selector: 'app-alert',
  templateUrl: './alert.component.html',
  styleUrls: ['./alert.component.css']
})
export class AlertComponent {
  isAlertVisible: boolean = true;

  hideAlert() {
    this.isAlertVisible = false;
  }
}
