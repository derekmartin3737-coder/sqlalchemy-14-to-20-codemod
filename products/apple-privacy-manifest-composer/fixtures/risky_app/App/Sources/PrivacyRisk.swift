import Foundation
import UIKit

final class PrivacyRisk {
    func readSettings() -> String? {
        return UserDefaults.standard.string(forKey: "account-mode")
    }

    func readFileDate(url: URL) throws -> Date? {
        let values = try url.resourceValues(forKeys: [.contentModificationDateKey])
        return values.contentModificationDate
    }

    func readDiskSpace(url: URL) throws -> Int64? {
        return try url.resourceValues(forKeys: [.volumeAvailableCapacityKey])
            .volumeAvailableCapacity
    }

    func uptime() -> TimeInterval {
        return ProcessInfo.processInfo.systemUptime
    }

    func keyboards() -> [UITextInputMode] {
        return UITextInputMode.activeInputModes
    }
}
