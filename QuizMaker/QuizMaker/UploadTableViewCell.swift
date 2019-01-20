//
//  UploadTableViewCell.swift
//  QuizMaker
//
//  Created by Nene Yamasaki on 20/01/2019.
//  Copyright © 2019 Nene Yamasaki. All rights reserved.
//

import UIKit

class UploadTableViewCell: UITableViewCell {
    var delegate:UploadCellDelegate?
    
    @IBAction func uploadButton(_ sender: Any) {
        self.delegate!.uploadData()
        
    }
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}

protocol UploadCellDelegate {
    func uploadData()
}
