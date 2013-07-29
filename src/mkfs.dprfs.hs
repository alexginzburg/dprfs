import Data.ConfigFile
import Control.Monad.Error
import System.Directory
import System.Environment
import System.Posix.Process
import System.Posix.Files
import System.IO

usage :: IO ()
usage = do
    me <- getProgName
    putStrLn $ "Usage: " ++ me ++ " <path>"

getconfig :: IO ()
getconfig = do
    rv <- runErrorT $
        do
        let x = cp
        buffersize <- get x  "general" "buffer_size"
        liftIO $ putStrLn buffersize
        meta_root  <- get x  "status"  "meta_root"
        liftIO $ putStrLn meta_root
        data_root  <- get x  "data"    "data_root"
        liftIO $ putStrLn data_root
    print rv

main :: IO ()
main = do
    args <- getArgs
    if length args /= 1
        then usage
        else do
            cwd <- getCurrentDirectory :: IO FilePath

            -- TODO: figure out monad error handling
            -- get settings
            cp <- join $ liftIO $ readfile emptyCP "server.conf"
            buffersize <- get cp "general" "buffer_size"
            meta_root  <- get cp "status"  "meta_root"
            data_root  <- get cp "data"    "data_root"

            newdir <- createDirectoryIfMissing meta_root ++ "/" ++ args
            setCurrentDirectory newdir

            content <- getContents stdin
            -- loop over bytes from std in (recursive func??)
            -- break if isEOF
            -- hash them
            -- hash dir, creat if needed
            -- write file fragment
            -- next!

            setCurrentDirectory cwd
            pid <- getProcessID

            let link_name = newdir ++ "/" ++ "base"
            let t_link_name = link_name ++ "." ++ pid
            createSymbolickLink base t_link_name
            rename t_link_name link_name
            
            let link_name = newdir ++ "/" ++ "top"
            let t_link_name = link_name ++ "." ++ pid
            createSymbolickLink base t_link_name
            rename t_link_name link_name
