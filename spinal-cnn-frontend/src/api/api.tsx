import axios from "axios";
import { AxiosError } from "axios";

const api = axios.create({
    baseURL: `${process.env.REACT_APP_BACKEND_URL}/api/`,
    timeout: 10000,
});


// TODO: Configure POST request to use API token to obtain content/register
/**
 *
 * @param content: JSON data, consisting of the JSON content that should be sent to the backend upon making a POST request
 * @param path: string, corresponding to the path for the POST request
 * @returns: JSON content, representing the result of the POST request
 */
export const postRequest = async (content: any, path: string) => {
    try {
        const response = await api.post(path, content);
        return response;
    } catch (error) {
        console.error(error);
        const axiosError = error as AxiosError;
        return { status: axiosError.status }
    }
};

export const postFiles = async (formData: FormData) => {
    const path = 'upload-files/';
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
