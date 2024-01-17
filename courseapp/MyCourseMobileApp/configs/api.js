import axios from 'axios'

export const endpoints = {
    'categories': '/categories/',
    'courses' : '/courses/'
}

const HOST = "https://thanhduong.pythonanywhere.com/"

export const authApi = () =>{
    return axios.create({
        baseURL: HOST, 
        headers: {
            'Authorization' : `Bearer ...`
        }
    })
}

export default axios.create({
    baseURL: HOST
})