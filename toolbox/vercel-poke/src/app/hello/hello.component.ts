import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

@Component({
  selector: 'app-hello',
  template: `<div>Hello {{value}}</div>`,
  templateUrl: './hello.component.html',
  styleUrls: ['./hello.component.css']
})

export class HelloComponent implements OnInit {

  url: any;
  status: any;
  statusText: any;
  headers: any;

  constructor(private http: HttpClient) {
  }

  ngOnInit(): void {
    this.http.get("https://echo.hyperdata.it", { responseType: 'text', observe: 'response' },).subscribe({
      next: data => {
        this.url = data['url']
        this.status = data['status']
        this.statusText = data['statusText']
        this.headers = JSON.parse(data['body']!) // non-null assertion
      },
      error: error => {
        console.error('error', error.message);
      },
    }); // wake up  vercel
  }
}




