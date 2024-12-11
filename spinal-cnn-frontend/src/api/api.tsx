import axios from "axios";
import { AxiosError } from "axios";

const api = axios.create({
    baseURL: `${process.env.REACT_APP_BACKEND_URL}/api/`,
    timeout: 10000,
});

export const postImage = async (formData: FormData) => {
    const path = 'scan-image/';
    try {
        const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/api/${path}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        return response;
    } catch (error) {
        console.error('Error uploading file:', error);
        const axiosError = error as AxiosError;
        return { status: axiosError.status }
    }
}
