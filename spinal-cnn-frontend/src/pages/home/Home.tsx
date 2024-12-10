import React, { useState } from 'react';
import './Home.css';
import { FilePond, registerPlugin } from 'react-filepond';
import FilePondPluginImagePreview from 'filepond-plugin-image-preview';
import FilePondPluginFileValidateType from "filepond-plugin-file-validate-type";
import { postFiles } from '../../api/api.tsx';
import 'filepond/dist/filepond.min.css';
import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css';

registerPlugin(FilePondPluginImagePreview)
registerPlugin(FilePondPluginFileValidateType);

export default function Home() {

    const [uploadedMedia, setUploadedMedia] = useState<File>()

    const handleMediaFiles = (newFiles: any) => {
        if (newFiles.length > 0) {
            setUploadedMedia(newFiles[0].file as File)
        }
    }

    const submitUpload = async () => {
        const formData = new FormData();

        // TODO: Do not submit unless LD file and Metadata is filled out
        if (uploadedMedia) {
            for (var i = 0; i < uploadedMedia.length; i++) {
                formData.append(`scan_image`, uploadedMedia[i])
            }
        }

        // TODO: Set screen to be unclickable while file is uploading

        const result = await postFiles(formData)
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
                        maxFiles={1}
                        name="files"
                        imagePreviewHeight={200}
                        acceptedFileTypes={["image/*"]} />
                    <div className="scan-output">
                        <p> Scan Output... </p>
                    </div>
                </div>
                <div className="classify-button">
                    <button onclick={submitUpload}>
                        <p> Detect </p>
                    </button>
                </div>
            </div>
        </div >
    )
}