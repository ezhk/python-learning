import '@babel/polyfill';
import 'whatwg-fetch';
import {app} from './js/main';
import './css/normalize.css';
import './css/style.css';

const appMain = new Vue(app);