import React, { useState } from 'react';
import './Home.css';
import { FilePond, registerPlugin } from 'react-filepond';
import FilePondPluginImagePreview from 'filepond-plugin-image-preview';
import FilePondPluginFileValidateType from "filepond-plugin-file-validate-type";
import { postImage } from '../../api/api.tsx';
import 'filepond/dist/filepond.min.css';
import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css';

registerPlugin(FilePondPluginImagePreview)
registerPlugin(FilePondPluginFileValidateType);

export default function Home() {

    const [uploadedMedia, setUploadedMedia] = useState<File>()
    const [scanResult, setScanResult] = useState<Boolean>(false)
    const [scanDescription, setScanDescription] = useState<String>("")

    const handleMediaFiles = (newFiles: any) => {
        if (newFiles.length > 0) {
            setUploadedMedia(newFiles[0].file as File)
        }
    }

    const handleRemoveFile = (error: any, newFile: any) => {
        setScanDescription("")
        setUploadedMedia()
    }

    const submitUpload = async () => {
        const formData = new FormData();

        if (uploadedMedia) {
            formData.append(`scan_image`, uploadedMedia)

            const result = await postImage(formData)
            if (result.status == 200) {
                if (result.data.scan_output) {
                    setScanDescription("You have Pneumonia.")
                }
                else {
                    setScanDescription("You DO NOT have Pneumonia!")
                }
            }
        }


    }

    return (
        <div className="home-page">
            <div className="header">
                <h1>Pneumonia Detector</h1>
                <h4>Bonerz</h4>
            </div>
            <div className="home-page-body">
                <div className="file-upload-div">
                    <FilePond
                        allowMultiple={true}
                        onupdatefiles={handleMediaFiles}
                        onremovefile={handleRemoveFile}
                        maxFiles={1}
                        name="files"
                        imagePreviewHeight={230}
                        acceptedFileTypes={["image/*"]} />
                    <div className="scan-output">
                        {(scanDescription.length > 0)
                            // ? <p className="black-text"> {scanDescription} </p>
                            ?
                            <img src={"http://localhost:8000/media/saliency_latest.jpeg"}></img>
                            :
                            <p> Scan Output... </p>
                        }
                    </div>
                </div>
                <div className="output-text">
                    {scanDescription && <p className="black-text"> <strong> Prediction: </strong>{scanDescription} </p>}
                </div>
                <div className="classify-button">
                    <button onClick={submitUpload}>
                        <p> Detect </p>
                    </button>
                </div>
            </div>
        </div >
    )
}