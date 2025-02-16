import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom'; // Import BrowserRouter
import App from './App';
import 'bulma/css/bulma.min.css';
import reportWebVitals from './reportWebVitals';
import {UserProvider} from './context/UserContext';
import { NotificationProvider } from './context/NotificationContext'; // Import NotificationProvider



const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(

  <BrowserRouter>
    <UserProvider>
        <NotificationProvider>
            <App />
        </NotificationProvider>
    </UserProvider>
  </BrowserRouter>,
);


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
