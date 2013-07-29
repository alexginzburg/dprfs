import Data.ConfigFile
import Control.Monad.Error
import System.Directory
import System.Environment

usage :: IO ()
usage = do
    name <- getProgName
    putStrLn $ "Usage: " ++ name ++ " <path>"

getconfig :: IO ()
getconfig = do
    rv <- runErrorT $
        do
        cp <- join $ liftIO $ readfile emptyCP "server.conf"
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
            getconfig
            print args
