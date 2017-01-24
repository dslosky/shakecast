import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions, URLSearchParams } from '@angular/http';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import { Observable } from 'rxjs/Observable';
import { ReplaySubject } from 'rxjs/ReplaySubject';

@Injectable()
export class NotificationHTMLService {
    public loadingData = new ReplaySubject(1);
    public notification = new ReplaySubject(1);
    public config = new ReplaySubject(1);

    constructor(private _http: Http) {}

    getNewEvent(name: string) {
        this.loadingData.next(true)
        this._http.get('/api/notification-html/new_event')
            .subscribe((result: Response) => {
                this.notification.next(result._body);
                this.loadingData.next(false)
            });
    }

    getNewShakeMap(name: string) {
        this.loadingData.next(true)
        this._http.get('/api/notification-html/shakemap')
            .subscribe((result: any) => {
                this.notification.next(result);
                this.loadingData.next(false)
            });
    }

    getConfigs(notType: string,
                name: string) {
        this.loadingData.next(true)
        this._http.get('/api/notification-config/' + notType + '/' + name)
            .map((result: Response) => result.json())
            .subscribe((result: any) => {
                this.config.next(result);
                this.loadingData.next(false)
            });
    }
}